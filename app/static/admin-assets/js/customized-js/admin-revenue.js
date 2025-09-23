function GetGraphData(yearly=false){
    let data = {
        'year': $('#years').val(),
    };
    
    if(!yearly){
        data['month_year'] = $('#month_year').val();
    }
  
    
}

