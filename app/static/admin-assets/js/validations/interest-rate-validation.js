
$("#add-interest").validate({
    ignore: [],
    rules: {
        minimum_amount: {
            required: true,
            min:0,
            },
        maximum_amount: {
            required: true,
            min:0,
            },
        interest_rate: {
            required: true,
            min:0,
            },
        additional_fees: {
            required: true,
            min:0,
            }
        },
    
    messages: {
        minimum_amount: {
            required: "Please enter minimum amount",
            },
        maximum_amount: {
            required: "Please enter maximum amount",
            },
        interest_rate: {
            required: "Please enter interest rate",
            },
        additional_fees: {
            required: "Please enter additional fees",
            }
    },
});


$("#edit-interest").validate({
    ignore: [],
    rules: {
        minimum_amount: {
            required: true,
            min:0,
            },
        maximum_amount: {
            required: true,
            min:0,
            },
        interest_rate: {
            required: true,
            min:0,
            },
        additional_fees: {
            required: true,
            min:0,
            }
        },
    
    messages: {
        minimum_amount: {
            required: "Please enter minimum amount",
            },
        maximum_amount: {
            required: "Please enter maximum amount",
            },
        interest_rate: {
            required: "Please enter interest rate",
            },
        additional_fees: {
            required: "Please enter additional fees",
            }
    },
});
