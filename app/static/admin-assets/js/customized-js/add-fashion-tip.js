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
        season: {
            required: true,
        },
        style: {
            required: true,
        },
        gender: {
            required: true,
        },
        content: {
            required:true
        },
        cover_image: {
            required: true,
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
            season: {
                required: "Please select season",
            },
            style: {
                required: "Please select style",
            },
            gender: {
                required: "Please select gender",
            },
            content: {
                required: "Please enter content",
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
        season: {
            required: true,
        },
        style: {
            required: true,
        },
        gender: {
            required: true,
        },
        content: {
            required:true,
        },
        
    },
    messages: {
            title: {
                required: "Please enter title",
            },
            category: {
                required: "Please select category",
            },
            season: {
                required: "Please select season",
            },
            style: {
                required: "Please select style",
            },
            gender: {
                required: "Please select gender",
            },
            content: {
                required: "Please enter description",
            },
           
        },
});    