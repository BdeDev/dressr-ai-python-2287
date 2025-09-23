$("#mobile-message-form").validate({
    rules: {
        assessbility_title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength: 100
        },
        assessbility_description: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength: 1000
        },
        
    },
    messages: {
        assessbility_title: {
            required: "Please enter title",
        },
        assessbility_description: {
            required: "Please enter description",
        },
    }
});  