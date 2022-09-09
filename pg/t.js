function dtest () {
  console.log("dtest()...")
  dtgtDiv = document.getElementById("dtgt")

  // var date_t = new Date("10/21/2014 08:00:00");
  var date_t = new Date("2022-09-05T22:53:48.200678Z");
  var date2_t = new Date("2022-09-05T22:53:47.200678Z");
  var outString = "";
  if (date_t > date2_t){
    outString = date2_t.toLocaleString();
  }
  else {
    outString = date_t.toLocaleString();
  }
  dtgtDiv.innerHTML=outString;
}
