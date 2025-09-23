$("#add-firebase").validate({
    ignore: [],
    rules: {
        fcm_file: {
            required: true,
            accept:'json'
            },
        project_id: {
            required:true
        },
    },
    messages: {
        fcm_file: {
            required: "Please select Fcm File",
            accept:'Please upload json file'
        },
        project_id: {
            required:"please enter project Id"
        },
    },
}); 

$("#edit-firebase").validate({
    ignore: [],
    rules: {
        fcm_file: {
            accept:'json'
            },
        project_id: {
            required:true
        },
        },
    messages: {
        fcm_file: {
            accept:'Please upload json file'
            },
        project_id: {
            required:"please enter project Id"
        },
    },
});  