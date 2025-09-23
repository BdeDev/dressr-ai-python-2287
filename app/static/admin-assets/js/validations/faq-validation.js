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

$("#add-faq").validate({
    ignore: [],
    rules: {
        question: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        answer: {
            ckrequired:true,
            ck_maxlength:true
        }
    },
    messages: {
        question: {
            required: "Please enter question",
        },
        answer: {
            ckrequired: "Please enter answer",
        }
    },
    errorPlacement: function (error, element) {
        if (element.attr("name") == "answer") {
            error.insertAfter("#cke_content");
        } else {
            error.insertAfter(element);
        }
    }
});   



$("#edit-faq").validate({
    ignore: [],
    rules: {
        question: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        answer: {
            ckrequired:true
        }
    },
    messages: {
        question: {
            required: "Please enter title",
        },
        answer: {
            ckrequired: "Please enter description"
        }
    },
    errorPlacement: function (error, element) {
        if (element.attr("name") == "answer") {
            error.insertAfter("#cke_content");
        } else {
            error.insertAfter(element);
        }
    }
});    