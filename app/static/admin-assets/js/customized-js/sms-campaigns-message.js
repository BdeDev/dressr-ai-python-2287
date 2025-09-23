
var count = 1;
function AddOnMobileField(){
    email_html = `
    <div class="col-lg-6 col-md-6 col-12 branch-div-${count}">
        <div class="input-group mb-3">
            <input  type="hidden" value="+91" id="country_code-${count}" name="country_code" class="form-control" maxlength="20">
            <input maxlength="15" type="text" id="mobile_number-${count}" sequence_count="${count}" onkeypress="return /[0-9]/i.test(event.key)" name="addon_mobile_no" class="form-control addon_mobile_added" placeholder="Mobile Number">
            <button class="btn btn-outline-danger" type="button" onclick="removeDiv(${count})" id="button-addon2">Remove</button>
        </div>
    </div>
    `
    $('#add-mobile-list').append(email_html)
    count = count + 1;

    // set value for country code option 
    set_country_code_option(count-1)
}


function set_country_code_option(id_count){
    input_id = "#mobile_number-" + id_count
    country_code_id = "#country_code-" + id_count
    $(input_id).intlTelInput({
        initialCountry: "in",
        separateDialCode: true,
     }).on('countrychange', function (e, countryData) {
        // on change of country code check for which country code is changed 
        sequence_count = $(e.currentTarget).attr('sequence_count')
        country_code_id = "#country_code-" + sequence_count
        updated_country_code = "+"+ $('.iti__selected-dial-code').text().split('+')[sequence_count]
        $(country_code_id).val(updated_country_code)
     });
}

function removeDiv(num){
    var remove_id = ".branch-div-" + num
    $(remove_id).remove()
}

function ValidateSendMessage(){
    is_valid = true
    error_message = ''
    // check for any user is selected on not 
    users_selected = $('.form-check-input:checked').length;
    
    // validate 

    if( users_selected < 1 && $('.addon_mobile_added').length < 1 ){
        is_valid = false
        error_message = 'Please select users or add addon mobile number'
    }

    // check for addon email address
    $('.addon_mobile_added').each(function(){
        mobile_value = $(this).val().trim()
        if(!mobile_value){
            is_valid = false
            error_message = 'Please enter mobile numbers to all fields'
            return ;
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