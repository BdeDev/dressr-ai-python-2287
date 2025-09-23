$("#edit-site").validate({
    rules: {
        domain: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
    },
    messages: {
        domain: {
            required: "Please enter domain",
        },
    },
});