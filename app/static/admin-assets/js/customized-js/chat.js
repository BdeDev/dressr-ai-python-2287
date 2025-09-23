function ScrollDownDiv(){
    let div_height = $('.ChatHistory')[0].scrollHeight
    $('.ChatHistory').scrollTop(div_height)
}

function ScrollToLastMessage(latest_msg_li_class){
    var div_height = $(`.${latest_msg_li_class}`).last().offset().top;
    $('.ChatHistory').scrollTop(div_height)
}


function SendMessage(url,chat_user_id,message,file=null){
    if(!message == "" || file){
        let formData = new FormData();
        formData.append('chat_user_id', chat_user_id);
        formData.append('message', message);
        formData.append('timezone', $('#timezone_id').val());
        if(file){
            formData.append('message_file', file);
        }
        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value,
            },
            data: formData,
            processData: false,
            contentType: false,
            async:false,
            success: function (data) {
                $('#messages-list').append(data.message)
                // make chat box and input file data empty 
                $('#chat-message').val("");
                $('#file_name').text("");
                let fileInput = document.getElementById('message_file');
                fileInput.value = '';

            }
        });
        ScrollDownDiv()

    }
    
}
// load unread mesages
let is_ready = true
function LoadUnreadMessages(url,chat_user_id){
    if(is_ready){
        is_ready = false
        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value,
            },
            data: { chat_user_id: chat_user_id,timezone: $('#timezone_id').val()},
            async:false,
            success: function (data) {
                $('#messages-list').append(data.data)
                if(data.is_message){
                    ScrollDownDiv()
                }
            },
        });
        is_ready = true
    }
}

// update user chat list 
function UserChatList(url,user_input,current_chat){
    $.ajax({
        url: url,
        type: "GET",
        data: { user_input: user_input,current_chat:current_chat,timezone: $('#timezone_id').val()},
        async:true,
        success: function (data) {
            $('#user-chat-list').html(data.data)
        },
    });

}

// load previous messages
let is_ready_previous = true
function LoadPreviousMessages(url,chat_user_id,latest_previous_message){
    if(is_ready_previous){
        is_ready_previous = false
        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value,
            },
            data: { chat_user_id: chat_user_id,latest_previous_message:latest_previous_message,timezone: $('#timezone_id').val()},
            async:false,
            success: function (data) {
                if(!data.data == ''){
                    $('#messages-list').prepend(data.data)
                    let latest_added = `latest-${latest_previous_message}`
                    ScrollToLastMessage(latest_added)

                    
                }
            },
        });
        is_ready_previous = true
    }

}
