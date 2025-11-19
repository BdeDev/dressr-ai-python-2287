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
                        start_time = moment.utc(start_date).local().format("LT");
                        let className = ['bg-success-subtle'];  // base class
                        // set new events
                        calendar.addEvent({
                            "id": items_data[i].id,
                            // "title": `Wear Items : ${followup_status} ( ${start_time} ) <br> Lead ID : ${followup_data[i].lead__lead_id}`,
                            "start": start_date_time,
                            "end": start_date_time,
                            "className": className,
                            // "status": followup_data[i].status,
                            "item_id": items_data[i].item_id,
                            "user_id": items_data[i].user_id,
                            "local_date_time": moment.utc(start_date).local().format("D MMMM YYYY, LT"),
                        });
                    }
                }
            },
        });

        
    },
    eventClick: function(info) {
        // on event click
        let selected_date = info.event._instance.range.start
        selected_date = moment.utc(selected_date).format("Do MMM YYYY");
        // check for consaltant or followup 
        item_id = info.event._def.extendedProps.item_id
        //console.log(selected_date,'clicked on event :  ',info.event._def.extendedProps)

        // Determine whether it's consultation or followup
        //let type = info.event._def.extendedProps.consultation_id ? "Consultation" : "WearItems";
        //let object_id = info.event._def.extendedProps.consultation_id || info.event._def.extendedProps.followup_id;
        //let lead_id = info.event._def.extendedProps.lead_id;
        //view_lead_url = `/lead-management/view-lead-info/${lead_id}/`

        // Consultation and Followup URLs
       // let object_redirect_url = '';
       // if (info.event._def.extendedProps.consultation_id) {
       //     object_redirect_url = `/lead-management/view-lead-consultation/${object_id}/`;
       // }
       // if (info.event._def.extendedProps.followup_id) {
       //     object_redirect_url = `/lead-management/view-follow-up/${object_id}/`;
       // }
//
       // consultation_status_dict = {1:'Pending',2:'Completed',3:'Cancelled'}

        //Swal.fire({
        //    title: `${type} Information`,
        //    html: `
        //        <div style="text-align:left;">
        //            <p class="mb-2"><strong>Date & Time :</strong> ${info.event._def.extendedProps.local_date_time}</p>
        //            <p class="mb-2"><strong>Status :</strong> ${consultation_status_dict[info.event._def.extendedProps.status]}</p>
        //            <p class="mb-2"><strong>Lead ID :</strong> ${info.event._def.extendedProps.custom_lead_id}</p>
        //            <div class="mt-4 text-center">
        //                <a href="${object_redirect_url}" class="btn btn-primary" style="margin-right:10px;">View ${type}</a>
        //                <a href="${view_lead_url}" class="btn btn-primary">View Lead </a>
        //            </div>
        //        </div>
        //    `,
        //    showConfirmButton: false,
        //    showCloseButton: true,
        //    position: 'center',
        //    
        //});
        
    }
    
});
calendar.render();