// admin help and support form

$("#set-loan-amount-form").validate({
    rules: {
        mxn_minimum_amount: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:1,
            max:1000,
        },
        mxn_maximum_amount: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:0,
            max:2000,
        },
        minimum_tenure: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:1,
            max:90,
        },
        maximum_tenure: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:2,
            max:365,
        },
        maximum_loan_installment: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:1,
            max:10,
        },
        
    },
    messages: {
        mxn_minimum_amount: {
            required: "Please enter minimum loan amount",
        },
        mxn_maximum_amount: {
            required: "Please enter maximum loan amount",
        },
        minimum_tenure: {
            required: "Please enter maximum loan tenure",
        },
        maximum_tenure: {
            required: "Please enter maximum loan tenure",
        },
        maximum_loan_installment: {
            required: "Please enter maximum loan installment",
        },
        
    },
}); 