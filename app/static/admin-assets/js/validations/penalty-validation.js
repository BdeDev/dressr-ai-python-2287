
$("#late-payment-penalty-form").validate({
    rules: {
        amount_percentage: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:0,
            max:100,
        },
    },
    messages: {
        amount_percentage: {
            required: "Please enter late payment penalty",
        },
        
    },
}); 