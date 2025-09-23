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

$("#add-feedback").validate({
    ignore: [],
    rules: {
        name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        content: {
            ckrequired:true
        },
        rating: {
                required: true,
                number: true,
                range:[1,5]
            },
    },
    messages: {
            name: {
                required: "Please enter name",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            rating: {
                required: "Please enter rating",
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



$("#edit-feedback").validate({
    ignore: [],
    rules: {
        name: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        content: {
            ckrequired:true
        },
        rating: {
                required: true,
                number: true,
                range:[1,5]
            },
    },
    messages: {
            name: {
                required: "Please enter name",
            },
            content: {
                ckrequired: "Please enter description",
                cke_maxlength:"Only 50 words are allowed!"
            },
            rating: {
                required: "Please enter rating",
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