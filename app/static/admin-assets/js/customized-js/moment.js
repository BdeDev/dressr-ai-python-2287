function ConvertDateTime(createdate, createtime,formate="MMMM D, YYYY h:mm A") {
    var d = createdate + "T" + createtime + "Z";
    const date = d;
    // const local = moment.utc(date).local().format("Do MMM YYYY hh:mm A");
    const local = moment.utc(date).local().format(formate);
    return local;
}

function ConvertDateTime1(createdate, createtime) {
    var d = createdate + "T" + createtime + "Z";
    const date = d;
    // const local = moment.utc(date).local().format("Do MMM YYYY");
    const local = moment.utc(date).local().format("MMMM D, YYYY");
    return local;
}
function ConvertDate(createdate, createtime) {
    var d = createdate + "T" + createtime + "Z";
    const date = d;
    const local = moment.utc(date).local().format("Do MMM YYYY");
    return local;
}
function ConvertTime(createdate, createtime) {
    var d = createdate + "T" + createtime + "Z";
    const date = d;
    const local = moment.utc(date).local().format("hh:mm A");
    return local;
}