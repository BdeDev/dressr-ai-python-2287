
var count = 1;



function AddOnEmailField(){
    email_html = `
    <div class="col-lg-6 col-md-6 col-12 branch-div-${count}">
        <div class="input-group mb-3">
            <input type="text" name="addon_email" class="form-control addon_email_added" placeholder="Email">
            <button class="btn btn-outline-danger" type="button" onclick="removeDiv(${count})" id="button-addon2">Remove</button>
        </div>
    </div>
    `
    $('#add-email-list').append(email_html)
    count = count + 1;
}


function removeDiv(num){
    var remove_id = ".branch-div-" + num
    $(remove_id).remove()
}


function ValidateSendEmail(){
    is_valid = true
    error_message = ''
    // check for any user is selected on not 
    users_selected = $('.form-check-input:checked').length;
    
    // validate 

    if( users_selected < 1 && $('.addon_email_added').length < 1 ){
        is_valid = false
        error_message = 'Please select users or add addon emails'
    }

    // check for addon email address
    $('.addon_email_added').each(function(){
        email_value = $(this).val().trim()
        if(!email_value){
            is_valid = false
            error_message = 'Please enter email to all fields'
            return ;
        }else{
            // validate for valid email 
            var email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!email_regex.test(email_value)) {
                is_valid = false
                error_message = 'Please enter valid email address'
                return ;
            }

        }
    })
    
    if(!is_valid){

        Swal.fire({
            // title: "Validation Error",
            text: error_message,
            icon: "error",
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Ok",
            showCancelButton: true,
            reverseButtons: true
        })

    }else{
        $('#send-campaign-email-form').submit()
    }

}