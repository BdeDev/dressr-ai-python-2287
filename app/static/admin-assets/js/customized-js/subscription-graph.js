function GetSubscriptionGraphData(){
        $.ajax({
            url: "/subscription/subscription-graph/",
            dataType: 'json',
            data: {
                'month': $('#months').val(),
                'year': $('#years').val(),
            },
            success: function (data) {
                Highcharts.chart("chart-container", data['subscribers']);
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

GetSubscriptionGraphData();
