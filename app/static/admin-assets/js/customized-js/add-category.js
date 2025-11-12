//Add Subscription form
$("#add-category").validate({
    ignore: [],
    rules: {
        name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:5,
            maxlength:50
        },
        description: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:5,
            maxlength:500
        }
    },
    messages: {
        name: {
            required: "Please enter name",
        },
        description: {
            required: "Please enter description"
        }
    },
});



// Update Subscription form
$("#update-category").validate({
    ignore: [],
    rules: {
        name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:5,
            maxlength:50
        },
        description: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:5,
            maxlength:500
        }
    },
    messages: {
        name: {
            required: "Please enter title",
        },
        description: {
            required: "Please enter description"
        }
    },
});