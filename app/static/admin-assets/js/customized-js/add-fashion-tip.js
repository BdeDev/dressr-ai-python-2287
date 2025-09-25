

$("#add-fashion-tip").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        category: {
            required: true,
        },
        content: {
            ckrequired:true
        },
        cover_image: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
            title: {
                required: "Please enter title",
            },
            category: {
                required: "Please select category",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            cover_image: {
                accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
            },
        },
});   



$("#edit-fashion-tip").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        category: {
            required: true,
        },
        content: {
            ckrequired:true
        },
        cover_image: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
            title: {
                required: "Please enter title",
            },
            category: {
                required: "Please select category",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            cover_image: {
                accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
            },
        },
});    