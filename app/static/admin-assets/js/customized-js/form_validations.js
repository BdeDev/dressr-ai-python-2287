

function GetContactId(id,email){
    $('#contactus_id').val(id);
    $('#reply_id').text(email);
}
$.validator.addMethod(
    "youtube_url",
    function(value, element) {
        if(value.trim().startsWith('https://www.youtube.com/watch?v=') == false){
            return false;
        }
        else{
            return true;
        }
    },
    "Please enter valid youtube url."
);
// login validation
$("#login").validate({
    rules: {
        username: {
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
            }
        },
    },
    messages: {
        username: {
            required: "Please enter your email address",
            
        },
        password: {
            required: "Please enter password",
            minlength: "At least 8 characters required!",
            maxlength: "At most 35 characters only!"
        },
    }
});

function changetype(){
    if ($("#password").attr('type') == "password"){
        document.getElementById("password").type = "text";
    }
    else{
        document.getElementById("password").type = "password";
    }
}
// forget password validation
$("#forget_password").validate({
    rules: {
        email: {
            required: true,
            email: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
    },
    messages: {
        email: {
            required: "Please enter email address",
        },
    }
});

// add Booster plan
$("#add-booster").validate({
    ignore: [],
    rules: {
        days: {
            required: true,
        },
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        price: {
            required: true,
            min:1,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
    },
    messages: {
        days: {
            required: "Please select validity (number of days)",
        },
        title: {
            required: "Please enter title",
        },
        price: {
            required: "Please enter price",
        },
    },
}); 
//Add My Dressr TV Videos
$("#add-video").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        description: {
            required:true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        link: {
            required: true,
            youtube_url: true,
        },
        thumbnail: {
            required: true,
            extension: 'jpg|png|jpeg',
        },
    },
    messages: {
        title: {
            required: "Please enter title",
        },
        description: {
            required: "Please enter description",
        },
        link: {
            required: "Please enter url",
            youtube_url:"Please enter a valid youtube url"
        },
        thumbnail: {
            required: "Please upload thumbnail",
            extension:"Please upload file with valid mimetype(i.e. jpg,png,jpeg)"
        }
    },
});  

$("#edit-video").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        description: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        link: {
            required: true,
            youtube_url:true,
        },
        thumbnail: {
            required: true,
            extension: 'jpg|png|jpeg',
        },
    },
    messages: {
        title: {
            required: "Please enter title",
        },
        description: {
            required: "Please enter description"
        },
        link: {
            required: "Please enter link.",
            youtube_url: "Please enter valid youtube url.",
        },
        thumbnail: {
            required: "Please upload thumbnail",
            extension:"Please upload file with valid mimetype(i.e. jpg,png,jpeg)"
        }
    },
});   

// Reply to contact us form
$("#reply-user").validate({
    rules: {
        reply_message: {
            required: true,
            normalizer: function( value ) {
                return $.trim( value );
            }
        }
    },
    messages: {
        reply_message: {
            required: "Please enter reply message"
        }
    }
});

$("#edit-details").validate({
    rules: {
        address: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        email: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            email: true,
        },
        mobile_no: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
            number: true,
            minlength: 8,
            maxlength: 15,
        },
    },
    messages: {
        address: {
            required: "Please enter address"
        },
        email: {
            required: "Please enter your email address",
        },
        mobile_no: {
            required: "Please enter your mobile number",
            minlength: "Mobile number should be at least 8 digits",
            maxlength: "Mobile number should not be more than 15 digits",
        },
    }
});  

$("#edit-social-details").validate({
    rules: {
        facebook: {
            required: true
        },
        twitter: {
            required: true
        },
        google: {
            required: true
        },
        
    },
    messages: {
        facebook: {
            required: "Please enter valid facebook url"
        },
        twitter: {
            required: "Please enter valid twitter url"
        },
        google: {
            required: "Please enter valid google url"
        },
        
    }
}); 
//Add Blog
$("#add-header-images").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        images: {
            required: true,
            accept: "jpg,png,jpeg,gif"
        },
        interval_minutes: {
            required: true,
        },
    },
    messages: {
        title: {
            required: "Please enter title",
        },
        images: {
            required: "Please select blog images",
            accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
        },
        interval_minutes: {
            required: "Please enter interval minutes",
        },
    },
    errorPlacement: function (error, element) {
        if (element.attr("name") == "images") {
            $("#empty_image_error").html(error);
        }
        else {
            error.insertAfter(element);
        }
    },
});  

$("#edit-header-image").validate({
    ignore: [],
    rules: {
        category: {
            required: true,
        },
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        images: {
            accept: "jpg,png,jpeg,gif"
        },
        interval_minutes: {
            required: true,
        },
    },
    messages: {
        title: {
            required: "Please enter title",
        },
        images: {
            required: "Please select blog images",
            accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
        },
        interval_minutes: {
            required: "Please enter interval minutes",
        },
    },
    errorPlacement: function (error, element) {
        if (element.attr("name") == "images") {
            $("#empty_image_error").html(error);

        }
        else {
            error.insertAfter(element);
        }
    },
});   