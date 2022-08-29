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
function applyTime(id,tz_p) {
  // based on https://www.plus2net.com/javascript_tutorial/clock.php
  var d = new Date().toLocaleString("en-US", {timeZone: tz_p,  hour12: false, hour: '2-digit', minute:'2-digit'});
  document.getElementById(id).innerHTML = d;
  timeTimeout(id,tz_p);
}
function timeTimeout(id,tz_p) {
  var refresh=1000;
  mytime = setTimeout(applyTime,refresh,id,tz_p);
}
// Immediately invoked function to set the theme on initial load
(function () {
   if (localStorage.getItem('theme') === 'theme-dark') {
       setTheme('theme-dark');
   } else {
       setTheme('theme-light');
   }
})();
