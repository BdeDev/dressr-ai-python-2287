(function () {
    window.onpageshow = function(event) {
        if (event.persisted) {
            window.location.reload();
        }
    };
})();
function Loader(formID) {
    loader_html = `
    <div class="maindiv">
        <div>
            <div class="loadericon">
                <div class="outerCircle"></div>
                    <div class="icon logoname">
                        <img alt="" width="10" src="/static/admin-assets/images/favicon.ico" />
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
    if ($('#'+formID).length){
        if ($('#'+formID).valid()){
            $('body').append(loader_html);
            $('body').css('pointer-events','none');
            $('.btn').css('pointer-events','none');
        }
    }else{
        if(!this.event.ctrlKey){
            $('body').append(loader_html);
            $('body').css('pointer-events','none');
            $('.btn').css('pointer-events','none');
        }
    }
}