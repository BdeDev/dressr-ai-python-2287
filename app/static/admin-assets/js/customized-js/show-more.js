// for show more and show less

function ShowMoreContent(showCharacter){
    if($('.show-more-content').length > 1){
        showChar = showCharacter
        var ellipsestext = "...";
        var moretext = "Show more >";
        var lesstext = "Show less";
        $('.show-more-content').each(function () {
            var content = $(this).html();
            if (content.length > showChar) {
                var c = content.substr(0, showChar);
                var h = content.substr(showChar, content.length - showChar);
                var html = c + '<div class="moreellipses">' + ellipsestext + '&nbsp;</div><div class="morecontent"><div class="remaining-content">' + h + '</div>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></div>';
                $(this).html(html);
            }

        });

        $(".morelink").click(function () {
            if ($(this).hasClass("less")) {
                $(this).removeClass("less");
                $(this).html(moretext);
            } else {
                $(this).addClass("less");
                $(this).html(lesstext);
            }
            $(this).parent().prev().toggle();
            $(this).prev().toggle();
            return false;
        });
    }
    

}


ShowMoreContent(1000)