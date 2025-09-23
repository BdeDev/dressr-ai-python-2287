// admin help and support form

$("#manage-lock-days-form").validate({
    rules: {
        soft_lock: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:1,
            max:90,
        },
        moderate_lock: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:1,
            max:90,
        },
        full_lock: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:1,
            max:90,
        },
    },
    messages: {
        soft_lock: {
            required: "Please enter soft lock days",
        },
        moderate_lock: {
            required: "Please enter moderate lock days",
        },
        full_lock: {
            required: "Please enter full lock days",
        },
        
    },
}); 