$("#add-key").validate({
    rules: {
        account_sid: {
            required: true,
            },
        number: {
            required: true,
            },
        token: {
            required: true,
            },
        },        
    messages: {
        account_sid: {
            required: "Please enter account sid",
            },
        number: {
            required: "Please enter number",
            },
        token: {
            required: "Please enter token",
            },
    },
}); 


$("#edit-key").validate({
    rules: {
        account_sid: {
            required: true,
            },
        number: {
            required: true,
            },
        token: {
            required: true,
            },
        },        
    messages: {
        account_sid: {
            required: "Please enter account sid",
            },
        number: {
            required: "Please enter number",
            },
        token: {
            required: "Please enter token",
            },
    },
});   