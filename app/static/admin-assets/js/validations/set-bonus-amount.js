// admin help and support form

$("#set-bonus-amount-form").validate({
    rules: {
        welcome_bonus: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:1,
            max:1000,
        },
        referral_bonus: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number:true,
            min:0,
            max:1000,
        },
    },
    messages: {
        welcome_bonus: {
            required: "Please enter welcome bonus amount",
        },
        referral_bonus: {
            required: "Please enter referral bonus amount",
        },
        
    },
}); 