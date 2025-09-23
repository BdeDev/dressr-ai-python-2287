$("#add-page").validate({
    ignore: [],
    rules: {
        lg_logo: {
            required: true,
            extension: "jpg|jpeg|png|gif|",
            minImageWidth: 100
            },
        favicon: {
            required: true,
            extension: "ico"
            }
        },
    
    messages: {
        lg_logo: {
            required: "Please choose a logo",
            extension: "Please upload file in these format only (jpg, jpeg, png, gif)",
            minImageWidth: "fregr"
            },
        favicon: {
            required: "Please choose a favicon",
            extension: "Please upload file in these format only (ico)"
            }
    },
});  

