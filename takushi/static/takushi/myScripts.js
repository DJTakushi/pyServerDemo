// https://marcbruederlin.github.io/particles.js/
window.onload = function() {
  Particles.init({
    selector: '.background',
    speed:.5,
    connectParticles:true,
    color: "#7CB9E8",
  });
};

function setActiveNavLink(id){
  var element=document.getElementById(id);
  if (element != null){
    element.className+=" nav-link-active";
  }
  else{
    console.log("setActiveNavLink could not find the id to set active(?)")
  }
  console.log("ran setActiveNavLink")
}

// function to set a given theme/color-scheme
// from https://medium.com/@haxzie/dark-and-light-theme-switcher-using-css-variables-and-pure-javascript-zocada-dd0059d72fa2
function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
    console.log("document.documentElement.className = ",document.documentElement.className)
}
// function to toggle between light and dark theme
function toggleTheme() {
   if (localStorage.getItem('theme') === 'theme-dark'){
       setTheme('theme-light');
   } else {
       setTheme('theme-dark');
   }
}
function applyTimes() {
    // based on https://www.plus2net.com/javascript_tutorial/clock.php
  const timeClasses = document.getElementsByClassName("time");
  for (const time_e of timeClasses){
    const myTz = time_e.getAttribute("tz")
    if (myTz != null){
      var d = new Date((new Date().getTime())+1000*myTz)
      // old style using timezone names.  OpenWeahter only supports seconds.
      // var d_text = d.toLocaleString("en-US", {hour12: false, hour: '2-digit', minute:'2-digit'});
      var d_text = d.toISOString().slice(11,16);//time in ISO format
      time_e.innerHTML = d_text
    }
  }
  var refresh=1000;
  mytime = setTimeout(applyTimes,refresh);
}

async function updateCities(apiUrl) {
    console.log('updateCities()')
    const response = await fetch(apiUrl);
    const myJson = await response.json(); //extract JSON from the http response

    cityRows=document.getElementsByClassName("cityRow")
    var earliestTimestamp = new Date();
    for (const cityRow of cityRows){
      const cityName = cityRow.id;

      for(const jsonRow of myJson){
          if (jsonRow.name == cityName){
            var timeZone = jsonRow.tz;
            var timeZoneOffset = jsonRow.tz_int;
            var conditionIconLink = jsonRow.conditionIcon;
            var temp_c=jsonRow.temp_c.toFixed(2);
            var temp_f=jsonRow.temp_f.toFixed(2);
            var humidity=jsonRow.humidity;

            time_e = cityRow.getElementsByClassName("time")[0];
            tzAtt = time_e.setAttribute("tz",timeZoneOffset);

            conditionIcon_e = cityRow.getElementsByClassName("conditionIcon")[0];
            conditionIcon_e.src=conditionIconLink;

            temperature_e = cityRow.getElementsByClassName("temperature")[0]
            temperature_e.innerHTML = temp_c + " C<br>"+temp_f+" F"

            humidity_e = cityRow.getElementsByClassName("humidity")[0]
            humidity_e.innerHTML = humidity+"%"

            date_t = new Date(jsonRow.lastRefresh);
            if (date_t < earliestTimestamp){
              earliestTimestamp=date_t;
            }
            break;
          }
      }
    }
    finDataTimeStamp = document.getElementById("cityDataTimestamp");
    var captionText = "Refreshed "+earliestTimestamp.toLocaleString()
    captionText += " from <a href=\"https://openweathermap.org/api\">Open Weather Api</a>";
    finDataTimeStamp.innerHTML=captionText;
    var refresh=1000*5;
    mytime = setTimeout(updateCities,refresh,apiUrl);
}

async function updateFin(apiUrl) {
    console.log('updateFin()')
    const response = await fetch(apiUrl);
    const myJson = await response.json(); //extract JSON from the http response

    finRows=document.getElementsByClassName("finRow");
    var earliestTimestamp = new Date();
    for (const finRow of finRows){
      const symbolName = finRow.getAttribute("symbol");

      for(const jsonRow of myJson){
          if (jsonRow.name == symbolName){
            console.log(jsonRow)

            var regularMarketPrice = jsonRow.regularMarketPrice;
            var previousClose = jsonRow.previousClose;
            var currency = jsonRow.currency;
            var dateHistoric = jsonRow.dateHistoric;
            var closeHistoric = jsonRow.closeHistoric;

            recent_e = finRow.getElementsByClassName("recent")[0];
            recent_e.innerHTML= regularMarketPrice.toLocaleString('en-us', {style:'currency', currency:currency});

            movement_e = finRow.getElementsByClassName("movement")[0];
            var movement = (100*(regularMarketPrice-previousClose)/previousClose);
            var movement_t = movement.toFixed(2);
            movement_e.innerHTML=movement_t+"%";
            if (movement >= 0){
              movement_e.style.color="green";
            }
            else {
              movement_e.style.color="red";
            }

            annual_e = finRow.getElementsByClassName("annual")[0];
            annual = (100*(regularMarketPrice-closeHistoric)/closeHistoric);
            annual_t = annual.toFixed(2)+"%";
            annual_e.innerHTML = annual_t;
            if (annual >= 0){
              annual_e.style.color="green";
            }
            else {
              annual_e.style.color="red";
            }

            date_t = new Date(jsonRow.lastRefresh);
            if (date_t < earliestTimestamp){
              earliestTimestamp=date_t;
            }
            break;
          }
      }
    }
    finDataTimeStamp = document.getElementById("finDataTimestamp");
    finDataTimeStamp.innerHTML="Refreshed "+earliestTimestamp.toLocaleString();
    var refresh=1000*60;
    mytime = setTimeout(updateFin,refresh,apiUrl);
}


// Immediately invoked function to set the theme on initial load
(function () {
   if (localStorage.getItem('theme') === 'theme-dark') {
       setTheme('theme-dark');
   } else {
       setTheme('theme-light');
   }
})();
