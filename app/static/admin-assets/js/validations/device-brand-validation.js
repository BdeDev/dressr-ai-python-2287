
$("#device-brand-form").validate({
    ignore: [],
    rules: {
        brand_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength:100,
            },
        
        },
    
    messages: {
        brand_name: {
            required: "Please enter brand name",
        },
       
       
    },
});


$("#edit-device-brand-form").validate({
    ignore: [],
    rules: {
        brand_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength:100,
            },
        
        },
    
    messages: {
        brand_name: {
            required: "Please enter brand name",
        },
       
       
    },
});

// to add Phone Models
$("#add-phone-model-form").validate({
    ignore: [],
    rules: {
        model_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength:100,
        },
        device_category: {
            required: true,
        },
    },
    messages: {
        model_name: {
            required: "Please enter model name",
        },
        device_category: {
            required: "Please select device category",
        },
    },
});


// to add Phone Models
$("#edit-phone-model-form").validate({
    ignore: [],
    rules: {
        model_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength:100,
        },
        device_category: {
            required: true,
        },
    },
    messages: {
        model_name: {
            required: "Please enter model name",
        },
        device_category: {
            required: "Please select device category",
        },
    },
});
