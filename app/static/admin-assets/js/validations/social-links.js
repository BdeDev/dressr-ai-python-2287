// add social links form 

$("#social-link-form").validate({
    rules: {
        facebook: {
            url: true
        },
        instagram: {
            url: true
        },
        twitter: {
            url: true
        }
    },
    messages: {
        facebook: {
            url:"Please enter valid link"
        },
        instagram: {
            url:"Please enter valid link"
        },
        twitter: {
            url:"Please enter valid link"
        },
    },
}); 