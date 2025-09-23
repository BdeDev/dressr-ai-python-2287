// admin help and support form

$("#edit_website_contact").validate({
    rules: {
        mobile_no: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            minlength:8,
            maxlength:15,
        },
        email: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            email:true
        },
        website: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            url: true
        },
        address: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:3,
            maxlength:100,
        }
    },
    messages: {
        mobile_no: {
            required: "Please mobile number",
            minlength:"Mobile number should be at least 8 digits",
            maxlength:"Mobile number should not be more than 15 digits",
        },
        email: {
            required: "Please enter email address",
            email:"Please enter valid email address"
        },
        website: {
            required: "Please enter website link",
            url:"Please enter valid website link"
        },
        address: {
            required: "Please enter address",
        },
    },
}); 