var scriptTag = document.currentScript;
var calender_initial_date = scriptTag.dataset.calender_initial_date;
var user_id = scriptTag.dataset.user_id;
var calender_url = scriptTag.dataset.calender_url;

Date.prototype.addDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    editable: false,
    droppable: false,
    selectable: true,
    navLinks: false,
    events: [],
    eventOrder:'start',
    initialDate: calender_initial_date,
    dayMaxEventRows: true, // for all non-TimeGrid views
    views: {
        timeGrid: {
            dayMaxEventRows: 6 // adjust to 6 only for timeGridWeek/timeGridDay
        }
    },
    headerToolbar: {
        right: 'prev,next today',
        center: 'title',   // <-- Month/Year will appear here
        left: ''
    },
    select:function( selectionInfo ){
        let selected_date = selectionInfo.start
        console.log(selected_date,'selected date')

        
    },
    eventContent: function(arg) {
        // to convert title into html
        return {
        html:  arg.event.title
        }
    },
    datesSet:function( dateInfo ){
        let current_date = dateInfo.start
        current_date = current_date.addDays(10)
        console.log(current_date,'dataset ')

        // on month change load specific month followup and consultant data 
        
        $.ajax({
            url: calender_url,
            type: "GET",
            data: { user_id:user_id,month:current_date.getMonth()+1,year:current_date.getFullYear()},
            async:false,
            success: function (data) {
                // clear all events
                calendar.removeAllEvents();
                // adding followup data 
                items_data = data.items_data
                if(items_data.length > 0){
                    for(let i=0; i < items_data.length ; i++){
                        let start_date =  items_data[i].worn_on
                        start_date_time = moment.utc(start_date).local().format("YYYY-MM-DD");

                        calendar.addEvent({
                            "id": items_data[i].id,
                            //"title":`Items : ${items_data[i].item__image}` ,
                            "start": start_date_time,
                            "end": start_date_time,
                            "image": window.location.origin + "/media/"+items_data[i].item__image,
                            "local_date_time": moment.utc(start_date).local().format("D MMMM YYYY, LT"),
                        });

                    }
                }
            },
        });
    },
    eventDidMount: function(info) {
    if (info.event.extendedProps.image) {
        let imageUrl = info.event.extendedProps.image;

        // Remove default event text
        info.el.innerHTML = "";

        let img = document.createElement("img");
        img.src = imageUrl;
        img.style.width = "150px";
        img.style.height = "120px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "6px";

        info.el.appendChild(img);
    }
}

});
calendar.render();

