CKEDITOR.replace('content',{
    disallowedContent:'img'
});

jQuery.validator.addMethod("ck_maxlength", function (value, element) {  
    var idname = $(element).attr('id');  
    var editor = CKEDITOR.instances[idname];  
    var ckValue = GetTextFromHtml(editor.getData()).replace(/<[^>]*>/gi, '').trim();
    if (ckValue.length === 0 ) {    
        $(element).val(ckValue);
    }else {  
        $(element).val(editor.getData());
    }
    return $(element).val().split(" ").length < 500;
}, "Only 500 words allowed!");  

$("#add-testimonial").validate({
    ignore: [],
    rules: {
        client_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        client_location: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        content: {
            ckrequired:true
        },
        client_image: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
            client_name: {
                required: "Please enter name",
            },
            client_location: {
                required: "Please enter location",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            client_image: {
                accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
            },
        },
    errorPlacement: function (error, element) {
        if (element.attr("name") == "answer") {
            error.insertAfter("#cke_content");
        } else {
            error.insertAfter(element);
        }
    }
});   



$("#edit-testimonial").validate({
    ignore: [],
    rules: {
        client_name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        client_location: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        client_image: {
            accept: "jpg,png,jpeg,gif"
        },
        content: {
            ckrequired:true
        },
    },
    messages: {
            client_name: {
                required: "Please enter name",
            },
            client_location: {
                required: "Please enter location",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            client_image: {
                accept: "Please upload file in these format only (jpg, jpeg, png, gif)"
            },
        },
    errorPlacement: function (error, element) {
        if (element.attr("name") == "answer") {
            error.insertAfter("#cke_content");
        } else {
            error.insertAfter(element);
        }
    }
});    