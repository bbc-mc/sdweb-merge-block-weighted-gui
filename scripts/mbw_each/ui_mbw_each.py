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

from scripts.mbw_each.merge_block_weighted_mod import merge
from scripts.mbw_util.preset_weights import PresetWeights
from scripts.mbw_util.merge_history import MergeHistory

presetWeights = PresetWeights()
mergeHistory = MergeHistory()


def on_ui_tabs():
    with gr.Column():
        with gr.Row():
            with gr.Column(variant="panel"):
                with gr.Row():
                    txt_multi_process_cmd = gr.TextArea(label="Multi Proc Cmd", placeholder="Keep empty if dont use.")
                html_output_block_weight_info = gr.HTML()
                with gr.Row():
                    btn_do_merge_block_weighted = gr.Button(value="Run Merge", variant="primary")
                    btn_clear_weighted = gr.Button(value="Clear values")
                    btn_reload_checkpoint_mbw = gr.Button(value="Reload checkpoint")
            with gr.Column():
                dd_preset_weight = gr.Dropdown(label="Preset_Weights", choices=presetWeights.get_preset_name_list())
                txt_block_weight = gr.Text(label="Weight_values", placeholder="Put weight sets. float number x 25")
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
            dd_model_A = gr.Dropdown(label="Model_A", choices=sd_models.checkpoint_tiles())
            dd_model_B = gr.Dropdown(label="Model_B", choices=sd_models.checkpoint_tiles())
            txt_model_O = gr.Text(label="(O)Output Model Name")
        with gr.Row():
            with gr.Column():
                sl_IN_A_00 = gr.Slider(label="IN_A_00", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_00")
                sl_IN_A_01 = gr.Slider(label="IN_A_01", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_01")
                sl_IN_A_02 = gr.Slider(label="IN_A_02", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_02")
                sl_IN_A_03 = gr.Slider(label="IN_A_03", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_03")
                sl_IN_A_04 = gr.Slider(label="IN_A_04", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_04")
                sl_IN_A_05 = gr.Slider(label="IN_A_05", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_05")
                sl_IN_A_06 = gr.Slider(label="IN_A_06", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_06")
                sl_IN_A_07 = gr.Slider(label="IN_A_07", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_07")
                sl_IN_A_08 = gr.Slider(label="IN_A_08", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_08")
                sl_IN_A_09 = gr.Slider(label="IN_A_09", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_09")
                sl_IN_A_10 = gr.Slider(label="IN_A_10", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_10")
                sl_IN_A_11 = gr.Slider(label="IN_A_11", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_A_11")
            with gr.Column():
                sl_IN_B_00 = gr.Slider(label="IN_B_00", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_00")
                sl_IN_B_01 = gr.Slider(label="IN_B_01", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_01")
                sl_IN_B_02 = gr.Slider(label="IN_B_02", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_02")
                sl_IN_B_03 = gr.Slider(label="IN_B_03", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_03")
                sl_IN_B_04 = gr.Slider(label="IN_B_04", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_04")
                sl_IN_B_05 = gr.Slider(label="IN_B_05", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_05")
                sl_IN_B_06 = gr.Slider(label="IN_B_06", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_06")
                sl_IN_B_07 = gr.Slider(label="IN_B_07", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_07")
                sl_IN_B_08 = gr.Slider(label="IN_B_08", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_08")
                sl_IN_B_09 = gr.Slider(label="IN_B_09", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_09")
                sl_IN_B_10 = gr.Slider(label="IN_B_10", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_10")
                sl_IN_B_11 = gr.Slider(label="IN_B_11", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_IN_B_11")
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
                sl_M_A_00 = gr.Slider(label="M_A_00", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_M_A_00")
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
                sl_M_B_00 = gr.Slider(label="M_B_00", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_M_B_00")
            with gr.Column():
                sl_OUT_A_11 = gr.Slider(label="OUT_A_11", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_11")
                sl_OUT_A_10 = gr.Slider(label="OUT_A_10", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_10")
                sl_OUT_A_09 = gr.Slider(label="OUT_A_09", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_09")
                sl_OUT_A_08 = gr.Slider(label="OUT_A_08", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_08")
                sl_OUT_A_07 = gr.Slider(label="OUT_A_07", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_07")
                sl_OUT_A_06 = gr.Slider(label="OUT_A_06", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_06")
                sl_OUT_A_05 = gr.Slider(label="OUT_A_05", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_05")
                sl_OUT_A_04 = gr.Slider(label="OUT_A_04", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_04")
                sl_OUT_A_03 = gr.Slider(label="OUT_A_03", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_03")
                sl_OUT_A_02 = gr.Slider(label="OUT_A_02", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_02")
                sl_OUT_A_01 = gr.Slider(label="OUT_A_01", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_01")
                sl_OUT_A_00 = gr.Slider(label="OUT_A_00", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_A_00")
            with gr.Column():
                sl_OUT_B_11 = gr.Slider(label="OUT_B_11", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_11")
                sl_OUT_B_10 = gr.Slider(label="OUT_B_10", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_10")
                sl_OUT_B_09 = gr.Slider(label="OUT_B_09", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_09")
                sl_OUT_B_08 = gr.Slider(label="OUT_B_08", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_08")
                sl_OUT_B_07 = gr.Slider(label="OUT_B_07", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_07")
                sl_OUT_B_06 = gr.Slider(label="OUT_B_06", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_06")
                sl_OUT_B_05 = gr.Slider(label="OUT_B_05", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_05")
                sl_OUT_B_04 = gr.Slider(label="OUT_B_04", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_04")
                sl_OUT_B_03 = gr.Slider(label="OUT_B_03", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_03")
                sl_OUT_B_02 = gr.Slider(label="OUT_B_02", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_02")
                sl_OUT_B_01 = gr.Slider(label="OUT_B_01", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_01")
                sl_OUT_B_00 = gr.Slider(label="OUT_B_00", minimum=0, maximum=1, step=0.01, value=0.5, elem_id="sl_OUT_B_00")

    # Footer
    gr.HTML(
        """
        <p style="font-size: 12px" align="right">
        <b>Merge Block Weighted</b> extension by <a href="https://github.com/bbc-mc" target="_blank">bbc_mc</a><br />
        <b>MBW Each</b> is experimental functions and <b>NO PROOF</b> of effectiveness.<br />
        You can try it by own, to dig more deeper into Abyss ...<br />
        </p>
        """
    )

    sl_A_IN = [
        sl_IN_A_00, sl_IN_A_01, sl_IN_A_02, sl_IN_A_03, sl_IN_A_04, sl_IN_A_05,
        sl_IN_A_06, sl_IN_A_07, sl_IN_A_08, sl_IN_A_09, sl_IN_A_10, sl_IN_A_11]
    sl_A_MID = [sl_M_A_00]
    sl_A_OUT = [
        sl_OUT_A_00, sl_OUT_A_01, sl_OUT_A_02, sl_OUT_A_03, sl_OUT_A_04, sl_OUT_A_05,
        sl_OUT_A_06, sl_OUT_A_07, sl_OUT_A_08, sl_OUT_A_09, sl_OUT_A_10, sl_OUT_A_11]

    sl_B_IN = [
        sl_IN_B_00, sl_IN_B_01, sl_IN_B_02, sl_IN_B_03, sl_IN_B_04, sl_IN_B_05,
        sl_IN_B_06, sl_IN_B_07, sl_IN_B_08, sl_IN_B_09, sl_IN_B_10, sl_IN_B_11]
    sl_B_MID = [sl_M_B_00]
    sl_B_OUT = [
        sl_OUT_B_00, sl_OUT_B_01, sl_OUT_B_02, sl_OUT_B_03, sl_OUT_B_04, sl_OUT_B_05,
        sl_OUT_B_06, sl_OUT_B_07, sl_OUT_B_08, sl_OUT_B_09, sl_OUT_B_10, sl_OUT_B_11]


    # Events
    def onclick_btn_do_merge_block_weighted(
        dd_model_A, dd_model_B, txt_multi_process_cmd,
        sl_IN_A_00, sl_IN_A_01, sl_IN_A_02, sl_IN_A_03, sl_IN_A_04, sl_IN_A_05,
        sl_IN_A_06, sl_IN_A_07, sl_IN_A_08, sl_IN_A_09, sl_IN_A_10, sl_IN_A_11,
        sl_M_A_00,
        sl_OUT_A_00, sl_OUT_A_01, sl_OUT_A_02, sl_OUT_A_03, sl_OUT_A_04, sl_OUT_A_05,
        sl_OUT_A_06, sl_OUT_A_07, sl_OUT_A_08, sl_OUT_A_09, sl_OUT_A_10, sl_OUT_A_11,
        sl_IN_B_00, sl_IN_B_01, sl_IN_B_02, sl_IN_B_03, sl_IN_B_04, sl_IN_B_05,
        sl_IN_B_06, sl_IN_B_07, sl_IN_B_08, sl_IN_B_09, sl_IN_B_10, sl_IN_B_11,
        sl_M_B_00,
        sl_OUT_B_00, sl_OUT_B_01, sl_OUT_B_02, sl_OUT_B_03, sl_OUT_B_04, sl_OUT_B_05,
        sl_OUT_B_06, sl_OUT_B_07, sl_OUT_B_08, sl_OUT_B_09, sl_OUT_B_10, sl_OUT_B_11,
        txt_model_O, sl_base_alpha, chk_verbose_mbw, chk_allow_overwrite,
        chk_save_as_safetensors, chk_save_as_half,
        radio_position_ids
    ):
        base_alpha = sl_base_alpha
        _weight_A = ",".join(
            [str(x) for x in [
                sl_IN_A_00, sl_IN_A_01, sl_IN_A_02, sl_IN_A_03, sl_IN_A_04, sl_IN_A_05,
                sl_IN_A_06, sl_IN_A_07, sl_IN_A_08, sl_IN_A_09, sl_IN_A_10, sl_IN_A_11,
                sl_M_A_00,
                sl_OUT_A_00, sl_OUT_A_01, sl_OUT_A_02, sl_OUT_A_03, sl_OUT_A_04, sl_OUT_A_05,
                sl_OUT_A_06, sl_OUT_A_07, sl_OUT_A_08, sl_OUT_A_09, sl_OUT_A_10, sl_OUT_A_11,
            ]])
        _weight_B = ",".join(
            [str(x) for x in [
                sl_IN_B_00, sl_IN_B_01, sl_IN_B_02, sl_IN_B_03, sl_IN_B_04, sl_IN_B_05,
                sl_IN_B_06, sl_IN_B_07, sl_IN_B_08, sl_IN_B_09, sl_IN_B_10, sl_IN_B_11,
                sl_M_B_00,
                sl_OUT_B_00, sl_OUT_B_01, sl_OUT_B_02, sl_OUT_B_03, sl_OUT_B_04, sl_OUT_B_05,
                sl_OUT_B_06, sl_OUT_B_07, sl_OUT_B_08, sl_OUT_B_09, sl_OUT_B_10, sl_OUT_B_11,
            ]])

        # debug output
        print( "#### Merge Block Weighted : Each ####")

        if (not dd_model_A or not dd_model_B) and txt_multi_process_cmd == "":
            _err_msg = f"ERROR: model not found. [{dd_model_A}][{dd_model_B}]"
            print(_err_msg)
            return gr.update(value=_err_msg)

        ret_html = ""
        if txt_multi_process_cmd != "":
            # need multi-merge
            _lines = txt_multi_process_cmd.split('\n')
            print(f"check multi-merge. {len(_lines)} lines found.")
            for line_index, _line in enumerate(_lines):
                if _line == "":
                    continue
                print(f"\n== merge line {line_index+1}/{len(_lines)} ==")
                _items = [x.strip() for x in _line.split(",") if x != ""]
                if len(_items) > 0:
                    ret_html += _run_merge(
                        weight_A=_weight_A, weight_B=_weight_B, model_0=dd_model_A, model_1=dd_model_B,
                        allow_overwrite=chk_allow_overwrite, base_alpha=base_alpha, model_Output=txt_model_O,
                        verbose=chk_verbose_mbw,
                        params=_items,
                        save_as_safetensors=chk_save_as_safetensors,
                        save_as_half=chk_save_as_half,
                        skip_position_ids=radio_position_ids
                        )
                else:
                    _ret = f"  multi-merge text found, but invalid params. skipped :[{_line}]"
                    ret_html += _ret
                    print(_ret)
        else:
            # normal merge
            ret_html += _run_merge(
                weight_A=_weight_A, weight_B=_weight_B, model_0=dd_model_A, model_1=dd_model_B,
                allow_overwrite=chk_allow_overwrite, base_alpha=base_alpha, model_Output=txt_model_O,
                verbose=chk_verbose_mbw,
                save_as_safetensors=chk_save_as_safetensors,
                save_as_half=chk_save_as_half,
                skip_position_ids=radio_position_ids
                )

        sd_models.list_models()
        print( "#### All merge process done. ####")

        return gr.update(value=f"{ret_html}")
    btn_do_merge_block_weighted.click(
        fn=onclick_btn_do_merge_block_weighted,
        inputs=[dd_model_A, dd_model_B, txt_multi_process_cmd]
            + sl_A_IN + sl_A_MID + sl_A_OUT + sl_B_IN + sl_B_MID + sl_B_OUT
            + [txt_model_O, sl_base_alpha, chk_verbose_mbw, chk_allow_overwrite]
            + [chk_save_as_safetensors, chk_save_as_half, radio_position_ids],
        outputs=[html_output_block_weight_info]
    )

    def _run_merge(weight_A, weight_B, model_0, model_1, allow_overwrite=False, base_alpha=0,
        model_Output="", verbose=False, params=[],
        save_as_safetensors=False,
        save_as_half=False,
        skip_position_ids=0,
        ):

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

        model_O = ""

        if params and len(params) > 0:
            for _item in params:
                # expect "O=merge/test02, IN_B_00 = 0.12345" as params=["O=merge/test02", "IN_B_00 = 0.12345"]
                if len(_item.split("=")) == 2:
                    _item_l = _item.split("=")[0].strip()
                    _item_r = _item.split("=")[1].strip()
                    if _item_r != "":
                        if _item_l.lower() == "model_a" or _item_l.lower() == "model_b":
                            _model_info = sd_models.get_closet_checkpoint_match(_item_r)
                            if _model_info:
                                _model_name = _model_info.title.split(" ")[0]
                                if _model_name and _model_name.strip() != "":
                                    if _item_l.lower() == "model_a":
                                        print(f"  * Model changed: {model_0} -> {_model_info.title}")
                                        model_0 = _model_info.title
                                    elif _item_l.lower() == "model_b":
                                        print(f"  * Model changed: {model_1} -> {_model_info.title}")
                                        model_1 = _model_info.title

                        elif _item_l.lower() == "preset_weights":
                            _weights = presetWeights.find_weight_by_name(_item_r)
                            if _weights != "" and len(_weights.split(',')) == 25:
                                print(f"  * Weights changed by preset-name: {_item_r}")
                                weight_B = _weights
                                weight_A = ",".join([str(1-float(x)) for x in _weights.split(',')])
                            else:
                                print(f"  * Weights change :canceled: [{_item_r}][{_weights}][{len(_weights.split(','))}]")

                        elif _item_l.lower() == "weight_values":
                            _weights = _item_r.strip()
                            if _weights != "" and len(_weights.split(' ')) == 25:  # this is work-around to use space as separator. Double-meaning issue on commna which already used as value separator and weights separator.
                                print(f"  * Weights changed: {_item_r}")
                                weight_B = _weights
                                weight_A = ",".join([str(1-float(x)) for x in _weights.split(' ')])
                            else:
                                print(f"  * Weights change :canceled: [{_item_r}][{_weights}][{len(_weights.split(','))}]")

                        elif _item_l.lower() == "base_alpha":
                            if float(_item_r) >= 0:
                                print(f"  * base_alpha changed: {base_alpha} -> {_item_r}")
                                base_alpha = float(_item_r)

                        elif _item_l.upper() == "O":
                            if _item_r.strip() != "":
                                _ret = validate_output_filename(_item_r.strip(), save_as_safetensors=save_as_safetensors, save_as_half=save_as_half)
                                print(f"  * Output filename changed:[{model_O}] -> [{_ret}]")
                                model_O = _ret

                        elif len(_item_l.split("_")) == 3:
                            _IMO = _item_l.split("_")[0]
                            _AB = _item_l.split("_")[1]
                            _NUM = _item_l.split("_")[2]

                            _index = int(_NUM)
                            _index = _index + 0 if _IMO == "IN" else _index
                            _index = _index + 12 if _IMO == "M" else _index
                            _index = _index + 13 if _IMO == "OUT" else _index

                            def _apply_val(key, weight, index, new_value):
                                _weight = [x.strip() for x in weight.split(",")]
                                _new_weight = _weight[:]
                                _new_weight[index] = new_value
                                _new_weight = ",".join(_new_weight)
                                print(f"  * weight_{key} changed:[{weight}]")
                                print(f"                  -> [{_new_weight}]")
                                return _new_weight

                            if _AB == "A":
                                weight_A = _apply_val(_AB, weight_A, _index, _item_r)
                            elif _AB == "B":
                                weight_B = _apply_val(_AB, weight_B, _index, _item_r)
                        else:
                            print(f"  * Waring: uncaught param found. ignored. [{_item_l}][{_item_r}]")

        #
        # Prepare params before run merge
        #

        # generate output file name from param
        model_A_info = sd_models.get_closet_checkpoint_match(model_0)
        _model_A_name = "" if not model_A_info else model_A_info.filename

        model_B_info = sd_models.get_closet_checkpoint_match(model_1)
        _model_B_name = "" if not model_B_info else model_B_info.filename

        if model_O == "":
            _a = os.path.splitext(os.path.basename(_model_A_name))[0]
            _b = os.path.splitext(os.path.basename(_model_B_name))[0]
            model_O = f"bw-merge-{_a}-{_b}-{base_alpha}" if model_Output == "" else model_Output
        model_O = validate_output_filename(model_O, save_as_safetensors=save_as_safetensors, save_as_half=save_as_half)
        output_file = os.path.join(shared.cmd_opts.ckpt_dir or sd_models.model_path, model_O)
        #
        # Check params
        #
        if not os.path.exists(os.path.dirname(output_file)):
            _err_msg = f"WARNING: target path not found: {os.path.dirname(output_file)}. skipped."
            print(_err_msg)
            return _err_msg + "<br />"
        if not allow_overwrite:
            if os.path.exists(output_file):
                _err_msg = f"WARNING: output_file already exists. overwrite not allowed. skipped."
                print(_err_msg)
                return _err_msg + "<br />"

        # debug output
        print(f"  model_0    : {model_0}")
        print(f"  model_1    : {model_1}")
        print(f"  model_Out  : {model_O}")
        print(f"  base_alpha : {base_alpha}")
        print(f"  output_file: {output_file}")
        print(f"  weight_A   : {weight_A}")
        print(f"  weight_B   : {weight_B}")
        print(f"  half       : {save_as_half}")
        print(f"  skip ids   : {skip_position_ids} : 0:None, 1:Skip, 2:Reset")

        result, ret_message = merge(
            weight_A=weight_A, weight_B=weight_B, model_0=model_0, model_1=model_1,
            allow_overwrite=allow_overwrite, base_alpha=base_alpha, output_file=output_file,
            verbose=verbose,
            save_as_safetensors=save_as_safetensors,
            save_as_half=save_as_half,
            skip_position_ids=skip_position_ids,
            )
        if result:
            ret_html = f"merged. {model_0} + {model_1} = {model_O} <br>"
            print("merged.")
        else:
            ret_html = ret_message
            print("merge failed.")


        # save log to history.tsv
        sd_models.list_models()
        model_A_info = sd_models.get_closet_checkpoint_match(model_0)
        model_B_info = sd_models.get_closet_checkpoint_match(model_1)
        model_O_info = sd_models.get_closet_checkpoint_match(os.path.basename(output_file))
        if hasattr(model_O_info, "sha256") and model_O_info.sha256 is None:
            model_O_info:CheckpointInfo = model_O_info
            model_O_info.sha256 = hashes.sha256(model_O_info.filename, "checkpoint/" + model_O_info.title)
        _names = presetWeights.find_names_by_weight(weight_B)
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
                base_alpha,
                weight_A,
                weight_B,
                weight_name
                )

        return ret_html

    btn_clear_weighted.click(
        fn=lambda: [gr.update(value=0.5) for _ in range(25*2)],
        inputs=[],
        outputs=[
            sl_IN_A_00, sl_IN_A_01, sl_IN_A_02, sl_IN_A_03, sl_IN_A_04, sl_IN_A_05,
            sl_IN_A_06, sl_IN_A_07, sl_IN_A_08, sl_IN_A_09, sl_IN_A_10, sl_IN_A_11,
            sl_M_A_00,
            sl_OUT_A_00, sl_OUT_A_01, sl_OUT_A_02, sl_OUT_A_03, sl_OUT_A_04, sl_OUT_A_05,
            sl_OUT_A_06, sl_OUT_A_07, sl_OUT_A_08, sl_OUT_A_09, sl_OUT_A_10, sl_OUT_A_11,
            sl_IN_B_00, sl_IN_B_01, sl_IN_B_02, sl_IN_B_03, sl_IN_B_04, sl_IN_B_05,
            sl_IN_B_06, sl_IN_B_07, sl_IN_B_08, sl_IN_B_09, sl_IN_B_10, sl_IN_B_11,
            sl_M_B_00,
            sl_OUT_B_00, sl_OUT_B_01, sl_OUT_B_02, sl_OUT_B_03, sl_OUT_B_04, sl_OUT_B_05,
            sl_OUT_B_06, sl_OUT_B_07, sl_OUT_B_08, sl_OUT_B_09, sl_OUT_B_10, sl_OUT_B_11,
        ]
    )

    def on_change_dd_preset_weight(dd_preset_weight):
        _weights = presetWeights.find_weight_by_name(dd_preset_weight)
        _ret = on_btn_apply_block_weight_from_txt(_weights)
        return [gr.update(value=_weights)] + _ret
    dd_preset_weight.change(
        fn=on_change_dd_preset_weight,
        inputs=[dd_preset_weight],
        outputs=[
            txt_block_weight,
            sl_IN_A_00, sl_IN_A_01, sl_IN_A_02, sl_IN_A_03, sl_IN_A_04, sl_IN_A_05,
            sl_IN_A_06, sl_IN_A_07, sl_IN_A_08, sl_IN_A_09, sl_IN_A_10, sl_IN_A_11,
            sl_M_A_00,
            sl_OUT_A_00, sl_OUT_A_01, sl_OUT_A_02, sl_OUT_A_03, sl_OUT_A_04, sl_OUT_A_05,
            sl_OUT_A_06, sl_OUT_A_07, sl_OUT_A_08, sl_OUT_A_09, sl_OUT_A_10, sl_OUT_A_11,
            sl_IN_B_00, sl_IN_B_01, sl_IN_B_02, sl_IN_B_03, sl_IN_B_04, sl_IN_B_05,
            sl_IN_B_06, sl_IN_B_07, sl_IN_B_08, sl_IN_B_09, sl_IN_B_10, sl_IN_B_11,
            sl_M_B_00,
            sl_OUT_B_00, sl_OUT_B_01, sl_OUT_B_02, sl_OUT_B_03, sl_OUT_B_04, sl_OUT_B_05,
            sl_OUT_B_06, sl_OUT_B_07, sl_OUT_B_08, sl_OUT_B_09, sl_OUT_B_10, sl_OUT_B_11,
            ]
    )

    def on_btn_reload_checkpoint_mbw():
        sd_models.list_models()
        return [gr.update(choices=sd_models.checkpoint_tiles()), gr.update(choices=sd_models.checkpoint_tiles())]
    btn_reload_checkpoint_mbw.click(
        fn=on_btn_reload_checkpoint_mbw,
        inputs=[],
        outputs=[dd_model_A, dd_model_B]
    )

    def on_btn_apply_block_weight_from_txt(txt_block_weight):
        if not txt_block_weight or txt_block_weight == "":
            return [gr.update() for _ in range(25*2)]
        _list = [x.strip() for x in txt_block_weight.split(",")]
        if(len(_list) != 25):
            return [gr.update() for _ in range(25*2)]
        return [gr.update(value=str(1-float(x))) for x in _list] + [gr.update(value=x) for x in _list]
    btn_apply_block_weithg_from_txt.click(
        fn=on_btn_apply_block_weight_from_txt,
        inputs=[txt_block_weight],
        outputs=[
            sl_IN_A_00, sl_IN_A_01, sl_IN_A_02, sl_IN_A_03, sl_IN_A_04, sl_IN_A_05,
            sl_IN_A_06, sl_IN_A_07, sl_IN_A_08, sl_IN_A_09, sl_IN_A_10, sl_IN_A_11,
            sl_M_A_00,
            sl_OUT_A_00, sl_OUT_A_01, sl_OUT_A_02, sl_OUT_A_03, sl_OUT_A_04, sl_OUT_A_05,
            sl_OUT_A_06, sl_OUT_A_07, sl_OUT_A_08, sl_OUT_A_09, sl_OUT_A_10, sl_OUT_A_11,
            sl_IN_B_00, sl_IN_B_01, sl_IN_B_02, sl_IN_B_03, sl_IN_B_04, sl_IN_B_05,
            sl_IN_B_06, sl_IN_B_07, sl_IN_B_08, sl_IN_B_09, sl_IN_B_10, sl_IN_B_11,
            sl_M_B_00,
            sl_OUT_B_00, sl_OUT_B_01, sl_OUT_B_02, sl_OUT_B_03, sl_OUT_B_04, sl_OUT_B_05,
            sl_OUT_B_06, sl_OUT_B_07, sl_OUT_B_08, sl_OUT_B_09, sl_OUT_B_10, sl_OUT_B_11,
        ]
    )
