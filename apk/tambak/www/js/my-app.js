// Init framework7
var app = new Framework7({
  // App root element
  root: '#app',
  // App Name
  name: 'Sensor CO',
  // App id
  id: 'id.plnm.sensorco',
  // Enable swipe panel
  panel: {
    swipe: 'left',
  },
  //pushState
  pushState: true,
  // Add default routes
  routes: [
	{
	  name:'main',
      path: '/',
	  url: './index.html',
    },
	{
      name: 'about',
      path: '/about/',
      url: './pages/about.html',
    },
	{
      path: '(.*)',
      url: './pages/404.html',
    },
  ],
  // Status bar
  statusbar: {
    androidOverlaysWebView: true,
  },
  //Card
  card: {
    hideNavbarOnOpe:false,
	hideToolbarOnOpen:false,
	swipeToClose:false,
	backrop:false,
	closeByBackdropClick:false,
  },
});
var mainView = app.views.create('.view-main', {
  url: '/'
});
// global vars
var $$ = Dom7;

function loadJSON() {
	//var data_file = "http://192.168.11.1/tambak/index.php/loaddata";
	var http_request = new XMLHttpRequest();
	try{
	   // Opera 8.0+, Firefox, Chrome, Safari
	   http_request = new XMLHttpRequest();
	}catch (e) {
	   // Internet Explorer Browsers
	   try{
		  http_request = new ActiveXObject("Msxml2.XMLHTTP");
			
	   }catch (e) {
		
		  try{
			 http_request = new ActiveXObject("Microsoft.XMLHTTP");
		  }catch (e) {
			 // Something went wrong
			 alert("Your browser broke!");
			 return false;
		  }
			
	   }
	}

	http_request.onreadystatechange = function() {

	   if (http_request.readyState == 4  ) {
		  // Javascript function JSON.parse to parse JSON data
		  var jsonObj = JSON.parse(http_request.responseText);

		  // jsonObj variable now contains the data structure and can
		  // be accessed as jsonObj.motion
		  document.getElementById("motion").innerHTML = jsonObj[0].deteksi;
		  document.getElementById("pir1").innerHTML = jsonObj[1].deteksi;
		  document.getElementById("pir2").innerHTML = jsonObj[2].deteksi;
		  
	   }
	   else{
	      document.getElementById("motion").innerHTML = "...";
		  document.getElementById("pir1").innerHTML = "...";
		  document.getElementById("pir2").innerHTML = "...";
	   }
	}

	http_request.open("POST", "http://192.168.11.1/tambak/index.php/loaddata", true);
	http_request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	http_request.setRequestHeader("Access-Control-Allow-Origin");
	http_request.send("tabel=motion");
}

window.setInterval(function () {
  //do something
  loadJSON();
},1000);