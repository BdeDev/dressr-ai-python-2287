function GetGraphData(){
    $.ajax({
        url: "/users/user-graph/",
        dataType: 'json',
        data: {
            'month': $('#months').val(),
            'year': $('#years').val(),
        },
        success: function (data) {
            Highcharts.chart("chart-container", data['users']);
            Highcharts.chart('chart-container-pie', data['pie_chart']);
            $('#selected_year').text(data['selected_year']);
            $('#selected_month').text(data['month_name']);
            $("#years option[value='"+data['selected_year']+"']").attr("selected","selected");
            $("#months option[value='"+data['selected_month']+"']").attr("selected","selected");
        }
    });
}
for (i = new Date().getFullYear(); i > new Date().getFullYear() - 5; i--)
{
    $('#years').append($('<option />').val(i).html(i));
    $('#r_years').append($('<option />').val(i).html(i));
    $('#r_years').append($('<option />').val(i).html(i));
}
GetGraphData();

// for sub admin graph





function GetGraphDataAffiliate(){
    $.ajax({
        url: "/ecommerce/affiliate-graph/",
        dataType: 'json',
        data: {
            'month': $('#months').val(),
            'year': $('#years').val(),
        },
        success: function (data) {
            Highcharts.chart("chart-container", data['users']);
            Highcharts.chart('chart-container-pie', data['pie_chart']);
            $('#selected_year').text(data['selected_year']);
            $('#selected_month').text(data['month_name']);
            $("#years option[value='"+data['selected_year']+"']").attr("selected","selected");
            $("#months option[value='"+data['selected_month']+"']").attr("selected","selected");
        }
    });
}
for (i = new Date().getFullYear(); i > new Date().getFullYear() - 5; i--)
{
    $('#years').append($('<option />').val(i).html(i));
    $('#r_years').append($('<option />').val(i).html(i));
    $('#r_years').append($('<option />').val(i).html(i));
}
GetGraphDataAffiliate();


// activity graph

var scriptTag = document.currentScript;
var user_id = scriptTag.dataset.user_id;
function GetActivityGraphData(){
    $.ajax({
        url: "/users/user-auditlog-activity-graph/",
        dataType: 'json',
        data: {
            'month': $('#activity_months').val(),
            'month': $('#activity_months').val(),
            'user_id': user_id,
        },
        success: function (data) {
            Highcharts.chart("activity-chart-container", data['users']);
            $('#activity_selected_year').text(data['selected_year']);
            $('#activity_selected_month').text(data['month_name']);
            $("#activity_years option[value='"+data['selected_year']+"']").attr("selected","selected");
            $("#activity_months option[value='"+data['selected_month']+"']").attr("selected","selected");
        }
    });
}
for (i = new Date().getFullYear(); i > new Date().getFullYear() - 5; i--)
{
    $('#activity_years').append($('<option />').val(i).html(i));
}



