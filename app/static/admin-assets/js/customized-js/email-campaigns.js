
var scriptTag = document.currentScript;
var logo_url = scriptTag.dataset.logo_url;
var description = scriptTag.dataset.description;
var query_param = scriptTag.dataset.query_param;
var protocol = scriptTag.dataset.protocol;
var domain = scriptTag.dataset.domain;


function GetTextFromHtml(html) {
    var dv = document.createElement("DIV");
    dv.innerHTML = html;
    return dv.textContent || dv.innerText || "";
}

$(document).ready(function () {
    if(!description){
        $('#content').html(`
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #fff; font-family: 'Open Sans', Arial, sans-serif; border-radius: 20px; box-shadow: 2px 2px 20px 4px rgba(0,0,0,0.07); max-width: 700px; margin: 40px auto;">
                <tr>
                    <td align="center" style="padding: 30px 10px 10px 10px; background: #14285a; border-radius: 0 0 0 0;">
                        <a href="${protocol}://${domain}" title="logo" target="_blank">
                            <img width="100" src="${protocol}://${domain}${logo_url}" title="logo" alt="logo" style="display:block; margin:auto;">
                        </a>
                    </td>
                </tr>
                <tr>
                    <td align="center" style="padding: 0 35px;">
                        <img src="${protocol}://${domain}/static/admin-assets/images/email-confirmed.png" style="width: 250px; max-width: 100%; height: auto; display: block; margin: 30px auto 0 auto;">
                    </td>
                </tr>
                <tr>
                    <td style="height:20px;">&nbsp;</td>
                </tr>
                <tr>
                    <td class="content-td" style="padding:0 35px;">
                        <h1 id="mail_title" name="mail_title" style="color: #000; font-weight: 500; margin: 0; font-size: 22px; font-family: 'Rubik',sans-serif; text-align:left;">
                            <b>Welcome to dressr ai</b>
                        </h1>
                        <p style="font-size:15px; color:#000; margin:0; line-height:24px; padding: 20px 0 20px 0; text-align:left;">
                            Dear <span style="text-decoration-line: underline;" id="email_user_name">User</span>,
                        </p>
                        <pre id="mail_description" style="font-size:15px; color:#000; margin:0; line-height:24px; padding-bottom:10px; text-align:left; white-space:pre-line; font-family: 'Open Sans', Arial, sans-serif; background:none; border:none;">Email Description</pre>
                    </td>
                </tr>
                <tr>
                    <td style="height:40px;">&nbsp;</td>
                </tr>
                <tr>
                    <td align="center" style="padding: 20px 0; border-top: 2px solid #cbcbcb4a; background-color: #14285a; border-radius:0 0 0 0;">
                        <p style="font-size:14px; color:#fff; line-height:18px; margin:0;">
                            Copyright  © <span id="full_year">2025</span>
                            <a style="color: #fff; text-decoration: none; font-weight: 600;" target="_blank" href="${protocol}://${domain}"> Dressr AI </a> | All Rights Reserved. Developed by
                            <a style="color: #fff; text-decoration: none; font-weight: 600;" href="https://toxsl.com/" target="_blank">TOXSL Technologies</a>
                        </p>
                    </td>
                </tr>
            </table>
        `)
        PreviewEmail()
    }
});
//CKEDITOR.replace('content');

CKEDITOR.replace('content', {
    allowedContent: true, // Allow all content
    height: 500,          // Set height to 700px

});

function PreviewEmail(){
    var idname = $(content).attr('id')
    var editor = CKEDITOR.instances[idname]
    // set email source code html into ifram  in iframe external css will not affect
    var iframe = document.getElementById('email_div');
    iframe.contentWindow.document.open();
    iframe.contentWindow.document.write(editor.getData());
    iframe.contentWindow.document.close();

    //$("#email_div").html(editor.getData())
}


$("#custome-email-form").validate({
    ignore: [],
    rules: {
        title: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            },
        },
        content: {
            ckrequired: true
        }
    },
    messages: {
        title: {
            required: "Please enter email subject",
        },
        content: {
            ckrequired: "Please enter email description"
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