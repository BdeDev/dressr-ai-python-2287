
$("#add-testimonials").validate({
    ignore: [],
    rules: {
        client_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        client_location: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        content: {
            ckrequired:true
        },
        client_image: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
            client_name: {
                required: "Please enter name",
            },
            client_location: {
                required: "Please enter location",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            client_image: {
                accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
            },
        },
   
});   



$("#edit-testimonial").validate({
    ignore: [],
    rules: {
        client_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        client_location: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        client_image: {
            accept: "jpg,png,jpeg,gif"
        },
        content: {
            ckrequired:true
        },
    },
    messages: {
            client_name: {
                required: "Please enter name",
            },
            client_location: {
                required: "Please enter location",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            client_image: {
                accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
            },
        },
});    