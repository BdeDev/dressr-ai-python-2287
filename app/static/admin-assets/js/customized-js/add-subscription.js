//Add Subscription form
$("#add-subscription-plan").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:5,
            maxlength:50
        },
        price: {
            required: true,
            min:1,
            max:10000,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true
        },
        validity: {
            required: true,
        },
        max_uploads: {
            required: true,
        },
        max_try_ons: {
            required: true,
        },
        max_shares: {
            required: true,
        },
        plan_type: {
            required: true,
        },
        month_year: {
            required: true,
        },
        description: {
            required: false,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:5,
            maxlength:500
        }
    },
    messages: {
        title: {
            required: "Please enter title",
        },
        price: {
            required: "Please enter price",
        },
        validity: {
            required: "Please select plan type",
        },
        max_uploads: {
            required: 'Please enter maximum uploads',
        },
        max_try_ons: {
            required: 'Please enter maximum try ons',
        },
        max_shares: {
            required: 'Please enter maximum shares',
        },
        plan_type: {
            required: 'Please select plan type',
        },
        month_year: {
            required: "Please select plan time period",
        },
        description: {
            required: "Please enter description"
        }
    },
});



// Update Subscription form
$("#update-subscription-plan").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:5,
            maxlength:50
        },
        price: {
            required: true,
            min:1,
            max:10000,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true
        },
        validity: {
            required: true,
        },
        max_uploads: {
            required: true,
        },
        max_try_ons: {
            required: true,
        },
        max_shares: {
            required: true,
        },
        plan_type: {
            required: true,
        },
        month_year: {
            required: true,
        },
        description: {
            required: false,
            normalizer: function (value) {
                return $.trim(value);
            },
            minlength:5,
            maxlength:500
        }
    },
    messages: {
        title: {
            required: "Please enter title",
        },
        price: {
            required: "Please enter price",
        },
        validity: {
            required: "Please select plan type",
        },
        max_uploads: {
            required: 'Please enter maximum uploads',
        },
        max_try_ons: {
            required: 'Please enter maximum try ons',
        },
        max_shares: {
            required: 'Please enter maximum shares',
        },
        plan_type: {
            required: 'Please select plan type',
        },
        month_year: {
            required: "Please select plan time period",
        },
        description: {
            required: "Please enter description"
        }
    },
});