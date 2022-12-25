//
// fix position of sliders
//

//
// UI
//
onUiUpdate(function () {
    // check Extension loaded
    if (gradioApp().querySelector("div#tab_mbw_each") == null ) return;

    // check already done
    //if (gradioApp().querySelector("#div_mdl_size_a") != null) return;

    // apply
    let _style = "min-width: min(200px, 100%); flex-grow: 1";
    gradioApp().querySelector("#sl_IN_A_00").parentElement.parentElement.setAttribute("style", _style)
    gradioApp().querySelector("#sl_IN_B_00").parentElement.parentElement.setAttribute("style", _style)
    gradioApp().querySelector("#sl_M_A_00").parentElement.parentElement.setAttribute("style", _style)
    gradioApp().querySelector("#sl_M_B_00").parentElement.parentElement.setAttribute("style", _style)
    gradioApp().querySelector("#sl_OUT_A_00").parentElement.parentElement.setAttribute("style", _style)
    gradioApp().querySelector("#sl_OUT_B_00").parentElement.parentElement.setAttribute("style", _style)
});
