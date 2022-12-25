# Merge block weighted Board
#
# extension of AUTOMATIC1111 web ui
#
# 2022/12/14 bbc_mc
#

import os
import gradio as gr

from modules import script_callbacks


from scripts.mbw import ui_mbw
from scripts.mbw_each import ui_mbw_each


#
# UI callback
#
def on_ui_tabs():

    with gr.Blocks() as main_block:
        with gr.Tab("MBW", elem_id="tab_mbw"):
            ui_mbw.on_ui_tabs()

        with gr.Tab("MBW Each", elem_id="tab_mbw_each"):
            ui_mbw_each.on_ui_tabs()

    # return required as (gradio_component, title, elem_id)
    return (main_block, "Merge Block Weighted", "merge_block_weighted"),

# on_UI
script_callbacks.on_ui_tabs(on_ui_tabs)
