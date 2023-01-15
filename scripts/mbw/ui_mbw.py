import gradio as gr
import os
import re

from modules import sd_models, shared
from tqdm import tqdm
try:
    from modules import hashes
    from modules.sd_models import CheckpointInfo
except:
    pass

from scripts.mbw.merge_block_weighted import merge
from scripts.mbw_util.preset_weights import PresetWeights
from scripts.mbw_util.merge_history import MergeHistory

presetWeights = PresetWeights()
mergeHistory = MergeHistory()


def on_ui_tabs():
    with gr.Column():
        with gr.Row():
            with gr.Column(variant="panel"):
                html_output_block_weight_info = gr.HTML()
                with gr.Row():
                    btn_do_merge_block_weighted = gr.Button(value="Run Merge", variant="primary")
                    btn_clear_weight = gr.Button(value="Clear values")
                    btn_reload_checkpoint_mbw = gr.Button(value="Reload checkpoint")
            with gr.Column():
                dd_preset_weight = gr.Dropdown(label="Preset Weights", choices=presetWeights.get_preset_name_list())
                txt_block_weight = gr.Text(label="Weight values", placeholder="Put weight sets. float number x 25")
                btn_apply_block_weithg_from_txt = gr.Button(value="Apply block weight from text", variant="primary")
                with gr.Row():
                    sl_base_alpha = gr.Slider(label="base_alpha", minimum=0, maximum=1, step=0.01, value=0)
                    chk_verbose_mbw = gr.Checkbox(label="verbose console output", value=False)
                    chk_allow_overwrite = gr.Checkbox(label="Allow overwrite output-model", value=False)
                with gr.Row():
                    with gr.Column(scale=3):
                        with gr.Row():
                            chk_save_as_half = gr.Checkbox(label="Save as half", value=False)
                            chk_save_as_safetensors = gr.Checkbox(label="Save as safetensors", value=False)
                    with gr.Column(scale=4):
                        radio_position_ids = gr.Radio(label="Skip/Reset CLIP position_ids", choices=["None", "Skip", "Force Reset"], value="None", type="index")
        with gr.Row():
            model_A = gr.Dropdown(label="Model A", choices=sd_models.checkpoint_tiles())
            model_B = gr.Dropdown(label="Model B", choices=sd_models.checkpoint_tiles())
            txt_model_O = gr.Text(label="Output Model Name")
        with gr.Row():
            with gr.Column():
                sl_IN_00 = gr.Slider(label="IN00", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_01 = gr.Slider(label="IN01", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_02 = gr.Slider(label="IN02", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_03 = gr.Slider(label="IN03", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_04 = gr.Slider(label="IN04", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_05 = gr.Slider(label="IN05", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_06 = gr.Slider(label="IN06", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_07 = gr.Slider(label="IN07", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_08 = gr.Slider(label="IN08", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_09 = gr.Slider(label="IN09", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_10 = gr.Slider(label="IN10", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_IN_11 = gr.Slider(label="IN11", minimum=0, maximum=1, step=0.01, value=0.5)
            with gr.Column():
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                gr.Slider(visible=False)
                sl_M_00 = gr.Slider(label="M00", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="mbw_sl_M00")
            with gr.Column():
                sl_OUT_11 = gr.Slider(label="OUT11", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_10 = gr.Slider(label="OUT10", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_09 = gr.Slider(label="OUT09", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_08 = gr.Slider(label="OUT08", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_07 = gr.Slider(label="OUT07", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_06 = gr.Slider(label="OUT06", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_05 = gr.Slider(label="OUT05", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_04 = gr.Slider(label="OUT04", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_03 = gr.Slider(label="OUT03", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_02 = gr.Slider(label="OUT02", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_01 = gr.Slider(label="OUT01", minimum=0, maximum=1, step=0.01, value=0.5)
                sl_OUT_00 = gr.Slider(label="OUT00", minimum=0, maximum=1, step=0.01, value=0.5)

    sl_IN = [
        sl_IN_00, sl_IN_01, sl_IN_02, sl_IN_03, sl_IN_04, sl_IN_05,
        sl_IN_06, sl_IN_07, sl_IN_08, sl_IN_09, sl_IN_10, sl_IN_11]
    sl_MID = [sl_M_00]
    sl_OUT = [
        sl_OUT_00, sl_OUT_01, sl_OUT_02, sl_OUT_03, sl_OUT_04, sl_OUT_05,
        sl_OUT_06, sl_OUT_07, sl_OUT_08, sl_OUT_09, sl_OUT_10, sl_OUT_11]

    # Events
    def onclick_btn_do_merge_block_weighted(
        model_A, model_B,
        sl_IN_00, sl_IN_01, sl_IN_02, sl_IN_03, sl_IN_04, sl_IN_05,
        sl_IN_06, sl_IN_07, sl_IN_08, sl_IN_09, sl_IN_10, sl_IN_11,
        sl_M_00,
        sl_OUT_00, sl_OUT_01, sl_OUT_02, sl_OUT_03, sl_OUT_04, sl_OUT_05,
        sl_OUT_06, sl_OUT_07, sl_OUT_08, sl_OUT_09, sl_OUT_10, sl_OUT_11,
        txt_model_O, sl_base_alpha, chk_verbose_mbw, chk_allow_overwrite,
        chk_save_as_safetensors, chk_save_as_half,
        radio_position_ids
    ):

        # debug output
        print( "#### Merge Block Weighted ####")

        _weights = ",".join(
            [str(x) for x in [
                sl_IN_00, sl_IN_01, sl_IN_02, sl_IN_03, sl_IN_04, sl_IN_05,
                sl_IN_06, sl_IN_07, sl_IN_08, sl_IN_09, sl_IN_10, sl_IN_11,
                sl_M_00,
                sl_OUT_00, sl_OUT_01, sl_OUT_02, sl_OUT_03, sl_OUT_04, sl_OUT_05,
                sl_OUT_06, sl_OUT_07, sl_OUT_08, sl_OUT_09, sl_OUT_10, sl_OUT_11
            ]])
        #
        if not model_A or not model_B:
            return gr.update(value=f"ERROR: model not found. [{model_A}][{model_B}]")

        #
        # Prepare params before run merge
        #

        # generate output file name from param
        model_A_info = sd_models.get_closet_checkpoint_match(model_A)
        if model_A_info:
            _model_A_name = model_A_info.model_name
        else:
            _model_A_name = ""
        model_B_info = sd_models.get_closet_checkpoint_match(model_B)
        if model_B_info:
            _model_B_info = model_B_info.model_name
        else:
            _model_B_info = ""

        def validate_output_filename(output_filename, save_as_safetensors=False, save_as_half=False):
            output_filename = re.sub(r'[\\|:|?|"|<|>|\|\*]', '-', output_filename)
            filename_body, filename_ext = os.path.splitext(output_filename)
            _ret = output_filename
            _footer = "-half" if save_as_half else ""
            if filename_ext in [".safetensors", ".ckpt"]:
                _ret = f"{filename_body}{_footer}{filename_ext}"
            elif save_as_safetensors:
                _ret = f"{output_filename}{_footer}.safetensors"
            else:
                _ret = f"{output_filename}{_footer}.ckpt"
            return _ret

        model_O = f"bw-merge-{_model_A_name}-{_model_B_info}-{sl_base_alpha}.ckpt" if txt_model_O == "" else txt_model_O
        model_O = validate_output_filename(model_O, save_as_safetensors=chk_save_as_safetensors, save_as_half=chk_save_as_half)

        _output = os.path.join(shared.cmd_opts.ckpt_dir or sd_models.model_path, model_O)

        if not chk_allow_overwrite:
            if os.path.exists(_output):
                _err_msg = f"ERROR: output_file already exists. overwrite not allowed. abort."
                print(_err_msg)
                return gr.update(value=f"{_err_msg} [{_output}]")
        print(f"  model_0    : {model_A}")
        print(f"  model_1    : {model_B}")
        print(f"  base_alpha : {sl_base_alpha}")
        print(f"  output_file: {_output}")
        print(f"  weights    : {_weights}")
        print(f"  skip ids   : {radio_position_ids} : 0:None, 1:Skip, 2:Reset")

        result, ret_message = merge(weights=_weights, model_0=model_A, model_1=model_B, allow_overwrite=chk_allow_overwrite,
            base_alpha=sl_base_alpha, output_file=_output, verbose=chk_verbose_mbw,
            save_as_safetensors=chk_save_as_safetensors,
            save_as_half=chk_save_as_half,
            skip_position_ids=radio_position_ids
            )

        if result:
            ret_html = "merged.<br>" \
                + f"{model_A}<br>" \
                + f"{model_B}<br>" \
                + f"{model_O}<br>" \
                + f"base_alpha={sl_base_alpha}<br>" \
                + f"Weight_values={_weights}<br>"
            print("merged.")
        else:
            ret_html = ret_message
            print("merge failed.")

        # save log to history.tsv
        sd_models.list_models()
        model_A_info = sd_models.get_closet_checkpoint_match(model_A)
        model_B_info = sd_models.get_closet_checkpoint_match(model_B)
        model_O_info = sd_models.get_closet_checkpoint_match(os.path.basename(_output))
        if hasattr(model_O_info, "sha256") and model_O_info.sha256 is None:
            model_O_info:CheckpointInfo = model_O_info
            model_O_info.sha256 = hashes.sha256(model_O_info.filename, "checkpoint/" + model_O_info.title)
        _names = presetWeights.find_names_by_weight(_weights)
        if _names and len(_names) > 0:
            weight_name = _names[0]
        else:
            weight_name = ""

        def model_name(model_info):
            return model_info.name if hasattr(model_info, "name") else model_info.title
        def model_sha256(model_info):
            return model_info.sha256 if hasattr(model_info, "sha256") else ""
        mergeHistory.add_history(
                model_name(model_A_info),
                model_A_info.hash,
                model_sha256(model_A_info),
                model_name(model_B_info),
                model_B_info.hash,
                model_sha256(model_B_info),
                model_name(model_O_info),
                model_O_info.hash,
                model_sha256(model_O_info),
                sl_base_alpha,
                _weights,
                "",
                weight_name
                )

        return gr.update(value=f"{ret_html}")
    btn_do_merge_block_weighted.click(
        fn=onclick_btn_do_merge_block_weighted,
        inputs=[model_A, model_B]
            + sl_IN + sl_MID + sl_OUT
            + [txt_model_O, sl_base_alpha, chk_verbose_mbw, chk_allow_overwrite]
            + [chk_save_as_safetensors, chk_save_as_half, radio_position_ids],
        outputs=[html_output_block_weight_info]
    )

    btn_clear_weight.click(
        fn=lambda: [gr.update(value=0.5) for _ in range(25)],
        inputs=[],
        outputs=[
            sl_IN_00, sl_IN_01, sl_IN_02, sl_IN_03, sl_IN_04, sl_IN_05,
            sl_IN_06, sl_IN_07, sl_IN_08, sl_IN_09, sl_IN_10, sl_IN_11,
            sl_M_00,
            sl_OUT_00, sl_OUT_01, sl_OUT_02, sl_OUT_03, sl_OUT_04, sl_OUT_05,
            sl_OUT_06, sl_OUT_07, sl_OUT_08, sl_OUT_09, sl_OUT_10, sl_OUT_11,
        ]
    )

    def on_change_dd_preset_weight(dd_preset_weight):
        _weights = presetWeights.find_weight_by_name(dd_preset_weight)
        _ret = on_btn_apply_block_weight_from_txt(_weights)
        return [gr.update(value=_weights)] + _ret
    dd_preset_weight.change(
        fn=on_change_dd_preset_weight,
        inputs=[dd_preset_weight],
        outputs=[txt_block_weight,
            sl_IN_00, sl_IN_01, sl_IN_02, sl_IN_03, sl_IN_04, sl_IN_05,
            sl_IN_06, sl_IN_07, sl_IN_08, sl_IN_09, sl_IN_10, sl_IN_11,
            sl_M_00,
            sl_OUT_00, sl_OUT_01, sl_OUT_02, sl_OUT_03, sl_OUT_04, sl_OUT_05,
            sl_OUT_06, sl_OUT_07, sl_OUT_08, sl_OUT_09, sl_OUT_10, sl_OUT_11,
            ]
    )

    def on_btn_reload_checkpoint_mbw():
        sd_models.list_models()
        return [gr.update(choices=sd_models.checkpoint_tiles()), gr.update(choices=sd_models.checkpoint_tiles())]
    btn_reload_checkpoint_mbw.click(
        fn=on_btn_reload_checkpoint_mbw,
        inputs=[],
        outputs=[model_A, model_B]
    )

    def on_btn_apply_block_weight_from_txt(txt_block_weight):
        if not txt_block_weight or txt_block_weight == "":
            return [gr.update() for _ in range(25)]
        _list = [x.strip() for x in txt_block_weight.split(",")]
        if(len(_list) != 25):
            return [gr.update() for _ in range(25)]
        return [gr.update(value=x) for x in _list]
    btn_apply_block_weithg_from_txt.click(
        fn=on_btn_apply_block_weight_from_txt,
        inputs=[txt_block_weight],
        outputs=[
            sl_IN_00, sl_IN_01, sl_IN_02, sl_IN_03, sl_IN_04, sl_IN_05,
            sl_IN_06, sl_IN_07, sl_IN_08, sl_IN_09, sl_IN_10, sl_IN_11,
            sl_M_00,
            sl_OUT_00, sl_OUT_01, sl_OUT_02, sl_OUT_03, sl_OUT_04, sl_OUT_05,
            sl_OUT_06, sl_OUT_07, sl_OUT_08, sl_OUT_09, sl_OUT_10, sl_OUT_11,
        ]
    )

