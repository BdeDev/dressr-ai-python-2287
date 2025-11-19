$("#reset-password").validate({
    rules: {
        password: {
            required: true, 
            minlength: 8,
            maxlength: 35,
            normalizer: function (value) {
                return $.trim(value);
            },
            strongpassword:"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{8,}$",
        },
        
    },
    messages: {
        password: {
            required: "Please enter password",
            minlength: "At least 8 characters required!",
            maxlength: "At most 35 characters only!",
            strongpassword:"Password must have one uppercase, lowercase, symbol and number",
        },
    }
});