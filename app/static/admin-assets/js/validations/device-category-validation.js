
$("#device-category-form").validate({
    ignore: [],
    rules: {
        category_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength:50,
            },
        maximum_loan_amount_in_mxn: {
            required: true,
            min:1,
            max:10000
            },
        
        },
    
    messages: {
        category_name: {
            required: "Please enter title",
            },
        maximum_loan_amount_in_mxn: {
            required: "Please enter maximum loan amount",
            },
       
    },
});

$("#edit-device-category-form").validate({
    ignore: [],
    rules: {
        category_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            maxlength:50,
            },
        maximum_loan_amount_in_mxn: {
            required: true,
            min:1,
            max:10000
            },
        
        },
    
    messages: {
        category_name: {
            required: "Please enter title",
            },
        maximum_loan_amount_in_mxn: {
            required: "Please enter maximum loan amount",
            },
       
    },
});
