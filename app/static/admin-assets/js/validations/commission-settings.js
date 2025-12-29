
function GetPerformanceGraphData(){
    $.ajax({
        url: "/ecommerce/affiliate-performance-graph/",
        dataType: 'json',
        data: {
            'month': $('#month_year').val(),
            'year': $('#years').val(),
            'user': $("#user_id").val()
        },
        
        success: function (data) {
            Highcharts.chart("chart-container", data['users']);
            $('#selected_year').text(data['selected_year']);
            $('#selected_month').text(data['month_name']);
            $("#years option[value='"+data['selected_year']+"']").attr("selected","selected");
            $("#months option[value='"+data['selected_month']+"']").attr("selected","selected");

            $('#total_Orders').text(data['total_Orders']);
            $('#total_commissions').text(data['total_commissions']);
            $('#total_sales').text(data['total_sales']);
            $('#total_clicks').text(data['total_clicks']);
        }
    });
}
for (i = new Date().getFullYear(); i > new Date().getFullYear() - 5; i--)
{
    $('#years').append($('<option />').val(i).html(i));
    $('#r_years').append($('<option />').val(i).html(i));
    $('#r_years').append($('<option />').val(i).html(i));
}
GetPerformanceGraphData();


$("#commission_settings").validate({
    rules: {
        commission_percentage: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        transactions: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
        minimum_payment_threshold: {
            required: true,
            normalizer: function (value) {
                return $.trim(value);
            }
        },
    },
    messages: {
        commission_percentage: {
            required: "Please enter commission settings",
        },
        transactions: {
            required: "Please enter number of transactions",
        },
        minimum_payment_threshold: {
            required: "Please enter minimum theshold for payment",
        },
    },
}); 