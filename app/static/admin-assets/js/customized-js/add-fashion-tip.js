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

$("#add-fashion-tip").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        category: {
            required: true,
        },
        content: {
            ckrequired:true
        },
        cover_image: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
            title: {
                required: "Please enter title",
            },
            category: {
                required: "Please select category",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            cover_image: {
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



$("#edit-fashion-tip").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        category: {
            required: true,
        },
        content: {
            ckrequired:true
        },
        cover_image: {
            accept: "jpg,png,jpeg,gif"
        },
    },
    messages: {
            title: {
                required: "Please enter title",
            },
            category: {
                required: "Please select category",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            cover_image: {
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