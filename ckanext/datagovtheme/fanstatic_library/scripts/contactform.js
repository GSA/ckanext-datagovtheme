jQuery(function ($) {
    const tpform_id = "fd986495";
    const tpform_js = "https://touchpoints.app.cloud.gov/touchpoints/"+tpform_id+".js";

    // load external touchpoint js script
    $.getScript(tpform_js, function () {
        console.log( "Touchpoint form is loaded." );
        set_form();
    });

    function set_form() {
        // unhide the button and set the click event
        $("#contact-btn").css('visibility', 'inherit').click(function () {
            // change the form location_code value
            if ($('article[data-package-name]')) {
                const dataset_name = $('article[data-package-name]').attr('data-package-name');
                $("#fba_location_code").val(dataset_name);
                $("#answer_04").val(dataset_name);
            }
        });
    }
});
