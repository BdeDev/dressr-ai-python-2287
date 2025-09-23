
$("#add-loan-offer").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            maxlength:200
        },
        minimum_amount: {
            required: true,
            number:true,
            min:0
        },
        maximum_amount: {
            required: true,
            number:true,
            min:0
        },
        interest_rate: {
            required: true,
            number:true,
            min:1,
            max:100,
        },
        image: {
            required: true,
            accept: "jpg,png,jpeg"
        },
        
        },
    
    messages: {
        title: {
            required: "Please enter title",
        },
        minimum_amount: {
            required: "Please enter minimum amount",
        },
        maximum_amount: {
            required: "Please enter maximum amount",
        },
        interest_rate: {
            required: "Please enter interest rate",
        },
        image: {
            required: "Please choose image",
            accept: "Please upload file in these format only (jpg, jpeg, png)"
        },
       
    },
});

$("#update-loan-offer").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            maxlength:200
        },
        minimum_amount: {
            required: true,
            number:true,
            min:0
        },
        maximum_amount: {
            required: true,
            number:true,
            min:0
        },
        interest_rate: {
            required: true,
            number:true,
            min:1,
            max:100,
        },
        image: {
            required: false,
            accept: "jpg,png,jpeg"
        },
        
        },
    
    messages: {
        title: {
            required: "Please enter title",
        },
        minimum_amount: {
            required: "Please enter minimum amount",
        },
        maximum_amount: {
            required: "Please enter maximum amount",
        },
        interest_rate: {
            required: "Please enter interest rate",
        },
        image: {
            required: "Please choose image",
            accept: "Please upload file in these format only (jpg, jpeg, png)"
        },
       
    },
});


