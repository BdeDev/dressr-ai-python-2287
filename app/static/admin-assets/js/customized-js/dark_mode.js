function toggleDarkMode() {
    let isDark = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
    var bulb_tag=$('#dark-mode-toggle');
    if (isDark){
        if (bulb_tag.hasClass("fas fa-lightbulb-on")){
            bulb_tag.removeClass("fas fa-lightbulb-on")
        }
        bulb_tag.addClass("fas fa-lightbulb")
        if($('#no-chat-selected')){
            $('#no-chat-selected').prop('src',"/static/admin-assets/images/default-chat-dark.jpg")
         }
    }
    else{
        if (bulb_tag.hasClass("fas fa-lightbulb")){
            bulb_tag.removeClass("fas fa-lightbulb")
        }
        bulb_tag.addClass("fas fa-lightbulb-on")
        if($('#no-chat-selected')){
           $('#no-chat-selected').prop('src',"/static/admin-assets/images/default-chat.png")
        }
    }
  }