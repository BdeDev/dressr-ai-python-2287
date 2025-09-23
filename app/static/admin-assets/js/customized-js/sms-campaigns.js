// add campaign message form validation 

$("#custome-sms-form").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength:150
        },
        content: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength:1000
        }
    },
    messages: {
        title: {
            required: "Please enter subject",
        },
        content: {
            required: "Please enter campaign message"
        }
    },
});