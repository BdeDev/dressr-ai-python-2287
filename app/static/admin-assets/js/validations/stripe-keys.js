$("#add-stripe-keys").validate({
        ignore: [],
        rules: {
            publish_key: {
                required: true,
                },
            secret_key: {
                required: true,
                },
            },
        messages: {
            publish_key: {
                required: "Please Enter Publish Key",
                },
            secret_key: {
                required: "Please Enter Secret Key",
                },
           
        },
    });  



$("#edit-stripe-keys").validate({
        ignore: [],
        rules: {
            publish_key: {
                required: true,
                },
            secret_key: {
                required: true,
                },
            },
        messages: {
            publish_key: {
                required: "Please Enter Publish Key",
                },
            secret_key: {
                required: "Please Enter Secret Key",
                },
        },
    }); 