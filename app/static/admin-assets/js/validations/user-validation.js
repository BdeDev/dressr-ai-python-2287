// password toggle 
function changetype(){
    if ($("#password").attr('type') == "password"){
        document.getElementById("password").type = "text";
    }
    else{
        document.getElementById("password").type = "password";
    }
}
// Edit User Profile
$("#EditProfile").validate({
    rules: {
        first_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        last_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        address: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        mobile_no: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        profile_pic: {
            accept: "jpg,png,jpeg,gif"
        },
        profile_pic1: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
        first_name: {
            required: "Please enter fitst name",
        },
        last_name: {
            required: "Please enter last name",
        },
        address: {
            required: "Please enter address",
        },
        mobile_no: {
            required: "Please enter phone number",
        },
        profile_pic: {
            accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
        },
        profile_pic1: {
            accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
        },
    }
});

// Change Email
$("#ChangeEmail").validate({
    rules: {
        new_email: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            email:true,
        },
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
        new_email: {
            required: "Please enter new email",
        },
        password: {
            required: "Please enter current password",
            minlength: "At least 8 characters required!",
            maxlength: "At most 35 characters only!",
            strongpassword:"Password must have one uppercase, lowercase, symbol and number",
        },
    }
});

// Change Email
$("#AddCard").validate({
    rules: {
        country_code: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        card_holder_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        card_number: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        card_expiry: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        cvv: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },  
    },
    messages: {
        country_code: {
            required: "Please select country",
        },
        card_holder_name: {
            required: "Please enter card holder name",
        },
        card_number: {
            required: "Please enter card number",
        },
        card_expiry: {
            required: "Please select expirty date",
        },
        cvv: {
            required: "Please enter cvv",
        },
        
    }
});

//send bulk message form validation
$("#add-message").validate({
    rules: {
        message: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
    },
    messages: {
        message: {
            required: "Please enter message.",
        },
    },
}); 

//Edit django site validation
$("#edit-site").validate({
    rules: {
        domain: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
    },
    messages: {
        domain: {
            required: "Please enter site domain.",
        },
    },
}); 


//Add Cusromer Validation
$("#add-user").validate({
    rules: {
        first_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        last_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        gender: {
            required: true,
        },
        email: {
            required: true,
            email: true,
            is_email_exists: ["{% url 'accounts:validations' %}",""],
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        mobile_no: {
            required: true,
            is_mobile_exists:["{% url 'accounts:validations' %}",""],
            minlength: 10,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        address: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        password: {
            required: true,
            minlength: 8,
            maxlength: 35,
            normalizer: function (value) {
                return $.trim(value);
            },
            strongpassword:"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{8,}$",
        },
        profile_pic: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
        first_name: {
            required: "Please enter first name",
        },
        last_name: {
            required: "Please enter last name",
        },
        gender: {
            required: "Please select gender",
        },
        email: {
            required: "Please enter email",
        },
        address: {
            required: "Please enter address",
        },
        mobile_no: {
            required: "Please enter mobile no",
            minlength: "At least 10 numbers required!",
        },
        password: {
            required: "Please enter password",
            minlength: "At least 8 characters required!",
            maxlength: "At most 35 characters only!",
            strongpassword:"Password must have one uppercase, lowercase, symbol and number",
        },
        profile_pic: {
            accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
        },
    }
});  
$("#edit-profile").validate({
    ignore:[],
    rules: {
        first_name:{
            required:true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        last_name:{
            required:true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        gender: {
            required: true,
        },
        address:{
            required:true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        email: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            email: true,
            is_email_exists: ["{% url 'accounts:validations' %}","{{user.id}}"],
        },
        mobile_no: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number: true,
            minlength: 8,
            maxlength: 15,
            is_mobile_exists:["{% url 'accounts:validations' %}","{{user.id}}"]
        },
        profile_pic: {
            accept: "jpg,png,jpeg",
        }
    },
    messages: {
        first_name: {
            required: "Please enter first name",
        },
        last_name: {
            required: "Please enter last name",
        },
        gender: {
            required: "Please select gender",
        },
        address: {
            required: "Please enter  address",
        },
        email: {
            required: "Please enter email address",
        },
        mobile_no: {
            required: "Please enter  mobile number",
            minlength: "Mobile number should be at least 8 digits",
            maxlength: "Mobile number should not be more than 15 digits",
        },
        profile_pic: {
            accept: "Please upload file in these format only (jpg, jpeg, png)",
        },
    },
});  
//End customer validation



//Add Subadmin validation
$("#add-subadmin").validate({
    rules: {
        first_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        last_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        gender: {
            required: true,
        },
        email: {
            required: true,
            email: true,
            is_email_exists: ["{% url 'accounts:validations' %}",""],
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        mobile_no: {
            required: true,
            is_mobile_exists:["{% url 'accounts:validations' %}",""],
            minlength: 10,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        address: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        password: {
            required: true,
            minlength: 8,
            maxlength: 35,
            normalizer: function (value) {
                return $.trim(value);
            },
            strongpassword:"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{8,}$",
        },
        profile_pic: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
        first_name: {
            required: "Please enter first name",
        },
        last_name: {
            required: "Please enter last name",
        },
        gender: {
            required: "Please select gender",
        },
        email: {
            required: "Please enter email",
        },
        address: {
            required: "Please enter address",
        },
        mobile_no: {
            required: "Please enter mobile no",
            minlength: "At least 10 numbers required!",
        },
        password: {
            required: "Please enter password",
            minlength: "At least 8 characters required!",
            maxlength: "At most 35 characters only!",
            strongpassword:"Password must have one uppercase, lowercase, symbol and number",
        },
        profile_pic: {
            accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
        },
    }
});    

$("#edit-subadmin").validate({
    ignore:[],
    rules: {
        first_name:{
            required:true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        last_name:{
            required:true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        gender: {
            required: true,
        },
        address:{
            required:true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        email: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            email: true,
            is_email_exists: ["{% url 'accounts:validations' %}","{{user.id}}"],
        },
        mobile_no: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number: true,
            minlength: 8,
            maxlength: 15,
            is_mobile_exists:["{% url 'accounts:validations' %}","{{user.id}}"]
        },
        profile_pic: {
            accept: "jpg,png,jpeg",
        }
    },
    messages: {
        first_name: {
            required: "Please enter first name",
        },
        last_name: {
            required: "Please enter last name",
        },
        gender: {
            required: "Please select gender",
        },
        address: {
            required: "Please enter  address",
        },
        email: {
            required: "Please enter email address",
        },
        mobile_no: {
            required: "Please enter  mobile number",
            minlength: "Mobile number should be at least 8 digits",
            maxlength: "Mobile number should not be more than 15 digits",
        },
        profile_pic: {
            accept: "Please upload file in these format only (jpg, jpeg, png)",
        },
    },
});   
//End Subadmin validation