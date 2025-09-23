
CKEDITOR.replace('content',{
    disallowedContent:'img'
});


$("#add-page").validate({
    ignore:[],
    rules: {
        type_id: {
            required: true,
        },
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        content: {
           ckrequired: true
        }
    },
    messages: {
        type_id: {
            required: "Please select type of page",
        },
        title: {
            required: "Please enter title",
        },
        content: {
            ckrequired: "Please enter description"
        }
    },
    errorPlacement: function (error, element) {
        if (element.attr("name") == "content") {
            error.insertAfter("#cke_content");
        } else {
            error.insertAfter(element);
        }
    }
});    


$("#edit-page").validate({
    ignore:[],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        content: {
            ckrequired: true,
            ck_maxlength:true

        }
    },
    messages: {
        title: {
            required: "Please enter title",
        },
        content: {
            ckrequired: "Please enter description",
            ck_maxlength:"Only 500 words are allowed!"
        }
    },
    errorPlacement: function (error, element) {
        if (element.attr("name") == "content") {
            error.insertAfter("#cke_content");
        } else {
            error.insertAfter(element);
        }
    }
});  