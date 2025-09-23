
$("#add-page").validate({
    ignore: [],
    rules: {
        email_host: {
            required: true,
            },
        email_port: {
            required: true,
            },
        use_tls: {
            required: true,
            },
        email_host_user: {
            required: true,
            email:true,
            },
        email_host_password: {
            required: true,
            },
        from_email: {
            required: true,
            }
        },
    
    messages: {
        email_host: {
            required: "Please enter email host",
            },
        email_port: {
            required: "Please enter email port",
            },
        use_tls: {
            required: "Please select tls",
            },
        email_host_user: {
            required: "Please enter host email",
            },
        from_email: {
            required: "Please enter from email",
            },
        email_host_password: {
            required: "Please enter email host password",
            }
    },
});


$("#edit-page").validate({
    ignore: [],
    rules: {
        email_host: {
            required: true,
            },
        email_port: {
            required: true,
            },
        use_tls: {
            required: true,
            },
        email_host_user: {
            required: true,
            },
        from_email: {
            required: true,
            },
        email_host_password: {
            required: true,
            }
        },
    
    messages: {
        email_host: {
            required: "Please enter email host",
            },
        email_port: {
            required: "Please enter email port",
            },
        use_tls: {
            required: "Please select tls",
            },
        email_host_user: {
            required: "Please enter host email",
            },
        from_email: {
            required: "Please enter from email",
            },
        email_host_password: {
            required: "Please enter email host password",
            }
    },

});