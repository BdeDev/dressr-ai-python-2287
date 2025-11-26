$("#add-activity-flags").validate({
    ignore: [],
    rules: {
        name: {
            required: true,
        },
        description: {
            required: true,
            minlength: 8,
            maxlength: 200,
            normalizer: function (value) {
                return $.trim(value);
            }
        }
    },
    messages: {
        name: {
            required: "Please Enter Name",
        },
        description: {
            required: "Please Enter Description",
        }
    }
});

$("#edit-activity-flags").validate({
    ignore: [],
    rules: {
        name: {
            required: true,
        },
        description: {
            required: true,
            minlength: 8,
            maxlength: 200,
            normalizer: function (value) {
                return $.trim(value);
            }
        }
    },
    messages: {
        name: {
            required: "Please Enter Name",
        },
        description: {
            required: "Please Enter Description",
        }
    }
});
