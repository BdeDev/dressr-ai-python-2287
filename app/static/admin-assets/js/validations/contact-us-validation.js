$("#contact-us").validate({
    rules: {
        full_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        email: {
            required: true,
            email: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        subject: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        message: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
    },
    messages: {
        full_name: {
            required: "Please enter full name",
        },
        email: {
            required: "Please enter email",
        },
        subject: {
            required: "Please enter subject"
        },
        message: {
            required: "Please enter message"
        },
    }
});  