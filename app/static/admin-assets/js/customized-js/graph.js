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


// for sub admin graph


function GetGraphDataSubAdmin(){
    $.ajax({
        url: "/users/sub-admin-user-graph/",
        dataType: 'json',
        data: {
            'sub_month': $('#sub_months').val(),
            'sub_year': $('#sub_years').val(),
        },
        success: function (data) {
            Highcharts.chart("sub-chart-container", data['users']);
            $('#sub_selected_year').text(data['sub_selected_year']);
            $('#sub_selected_month').text(data['sub_month_name']);
            $("#sub_years option[value='"+data['sub_selected_year']+"']").attr("selected","selected");
            $("#sub_months option[value='"+data['sub_selected_month']+"']").attr("selected","selected");
        }
    });
}
for (i = new Date().getFullYear(); i > new Date().getFullYear() - 5; i--)
{
    $('#sub_years').append($('<option />').val(i).html(i));
    $('#sub_r_years').append($('<option />').val(i).html(i));
}




function GetLoanGraphData() {
    $.ajax({
        url: "/loan-manager/loan-application-graph/",
        dataType: 'json',
        data: {
            'loan_month': $('#loan_months').val(),
            'loan_year': $('#loan_years').val(),
        },
        success: function(data) {
            Highcharts.chart("loan-chart-container", data['chart']);
            Highcharts.chart('chart-container-pie', data['pie_chart']);
            $('#loan_selected_year').text(data['loan_selected_year']);
            $('#loan_selected_month').text(data['loan_month_name']);
            $("#loan_years option[value='" + data['loan_selected_year'] + "']").attr("selected", "selected");
            $("#loan_months option[value='" + data['loan_selected_month'] + "']").attr("selected", "selected");
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}

for (let i = new Date().getFullYear(); i > new Date().getFullYear() - 5; i--) {
    $('#loan_years').append($('<option />').val(i).html(i));
    $('#loan_r_years').append($('<option />').val(i).html(i));
}


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
