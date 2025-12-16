$("#add-discount").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        
        store: {
            required: true,
        },
        target_sigment: {
            required: true,
        },
        image: {
            required: true,
        },
        start_date: {
            required:true
        },
        end_date: {
                required: true,
            },
        description: {
            required: true,
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
            title: {
                required: "Please enter title",
            },
          
            store: {
                required: "Please select store",
            },
            target_sigment: {
                required: "Please select sigment",
            },
            image: {
                required: "Please upload file in these format only (jpg, jpeg, png, gif)",
            },
            start_date: {
                required: "Please enter start date",
            },
            end_date: {
                required: "Please enter end date",
            },
            description: {
                accept: "Please enter description"
            },
        },
    });   



$("#edit-discount").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        
        store: {
            required: true,
        },
        target_sigment: {
            required: true,
        },
        image: {
            required: true,
        },
        start_date: {
            required:true
        },
        end_date: {
                required: true,
            },
        description: {
            required: true,
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
            title: {
                required: "Please enter title",
            },
          
            store: {
                required: "Please select store",
            },
            target_sigment: {
                required: "Please select sigment",
            },
            image: {
                required: "Please upload file in these format only (jpg, jpeg, png, gif)",
            },
            start_date: {
                required: "Please enter start date",
            },
            end_date: {
                required: "Please enter end date",
            },
            description: {
                accept: "Please enter description"
            },
        },
    });   