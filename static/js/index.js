
setTimeout(function(){
  document.querySelector(".preloader").style.display = "none";
}, 1000);

if (!sessionStorage.getItem('page_reloaded')) {
  sessionStorage.setItem('page_reloaded', true);
  location.reload();
}

let map, infoWindow;
// Create info

// REFER TO: https://developers.google.com/maps/documentation/javascript/examples/control-bounds-restriction#maps_control_bounds_restriction-javascript 
// NYC BOUNDS (PROGRAM IS NYC SPECIFIC )
// NOTE DO NOT DRASTICALLY CHANGE THE NORTH, SOUTH, WEST OR EAST OR ELSE IT WILL PAN OUT / ZOOM OUT TO MUCH
const NYC_BOUNDS = {
  north: 40.987577, 
  south: 40.477398, 
  west: -74.259090, 
  east: -73.800272,
};
const NYC_CENTER = { lat: 40.7128, lng: -74.0060 };

function initMap() {

  map = new google.maps.Map(document.getElementById("map"), {
    center: NYC_CENTER,
    restriction: {
      latLngBounds: NYC_BOUNDS,
      strictBounds: false,
    },
    zoom: 11,
    disableDefaultUI: true,
    mapTypeId: 'satellite' // NOTE FOR ESHAAN: CHANGED TO SATELLITE VIEW 
    // fullscreenControl: false
  });


  infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
  locationButton.textContent = "Current Location";
  locationButton.classList.add("center-button");
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(locationButton);
  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          //console.log(position.coords.latitude);

          //infoWindow.setPosition(pos);
          //infoWindow.setContent("Location found.");
          infoWindow.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
   });
   
   google.maps.event.addListener(map, 'dblclick', function(event){
    let marker = new google.maps.Marker({
        position: event.latLng,
        map: map,
        draggable: true,
        icon: {
          url:"http://maps.google.com/mapfiles/ms/icons/pink-dot.png"
        }
     });
  
     google.maps.event.addListener(marker,'dblclick', function(event){
        marker.setMap(null);
        
     });

    let geocoder = new google.maps.Geocoder();
    let latLng = event.latLng;
    
    // Send a geocoding request to Google Maps Geocoding API.
    geocoder.geocode({ location: latLng }, (results, status) => {
      if (status === google.maps.GeocoderStatus.OK) {
        // Extract the postal code (zipcode) from the geocoding results.
        const zipcode = findZipCodeInResults(results[0]);

        // Extract the exact latitude and longitude as strings.
        const latitude = latLng.lat().toString();
        const longitude = latLng.lng().toString();
    
        // Create an object with latitude, longitude, and zipcode.
        const locationData = {
          latitude: latitude,
          longitude: longitude,
          zipcode: zipcode
        };
        // Shade zipcode 10000 in red
    
        // Send the location data to the server using a fetch request.
        fetch('/add_data', {
          method: 'POST',
          credentials: 'include',
          body: JSON.stringify(locationData),
          headers: { 'Content-Type': 'application/json' }
        }).then(() => location.reload());
      }
    });
    
    // Helper function to find the zipcode from geocoding results.
    function findZipCodeInResults(geocodeResult) {
      for (let component of geocodeResult.address_components) {
        if (component.types.includes('postal_code')) {
          return component.short_name;
        }
      }
      return null; // Return null if no zipcode is found.
    }})
   
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}

window.initMap = initMap;

// FETCHED DATA FROM THE PARKINGMETERS CSV FILE
// NOTE FOR GROUP, CACHED CSV DATA (METER)
fetch('/cached_csv_data')
.then(response => response.json())
.then(data => {
    // Process and use the cached CSV data in your JavaScript code
    //console.log(typeof(data));
    //console.log(data.length);
    for(let i = 0; i < data.length; i++){
      (function(i) {

        //console.log(data[i]['Latitude']); // WAY TO GET LATITUDE DATA
        //console.log(data[i]);
        latitude = data[i]['Latitude']
        longitude = data[i]['Longitude']
        meterHours = data[i]['Meter_Hours']
        cellPay = data[i]['Pay By Cell Number']
        //console.log(latitude, longitude, cellPay, meterHours);

        let meterMarker = new google.maps.Marker({
          position: {lat: latitude, lng: longitude},
          icon: {
           url: "static/icons/parkingmeter.png"
            //url: "./static/Button_Icon_Green.svg.png"
          },
          map: map,
          draggable: false
       });

       // ADD IN INFORMATION 
       var infowindow = new google.maps.InfoWindow({
        content: "<h1 style='color: black; font-size: 15, font: Times New Roman'>Meter Parking!</h1> </br> <p style='color: black; font-size: 15, font: Times New Roman'> Meter Usage: " + meterHours + " </br> Pay By Phone: " + cellPay+  " </br> Note that this is from our  <b style='color: black'>database!</b> </p>"
       });
       
       meterMarker.addListener('mouseover', function() {
        infowindow.open(map, meterMarker);
       });

       meterMarker.addListener('mouseout', function() {
        infowindow.close();
       });
       
       ;})(i) // function (i) prevents the asynch info by keeping it all together 

    } // end {} for the for loop
    
});


let x;
// Fetch from the python file (check /data) (FETCHED FROM FLASK-SQL DATABASE)
fetch('/data')
.then(response => response.json())
.then(data => {
    //console.log(data);
//    const geocoder = new google.maps.Geocoder();

// Code below starts at 0 and goes till end of the data.length (note that this depends on how large)

    for(let i = 0; i < data.length; i++){
      
        let markerA = new google.maps.Marker({
          position: {lat: data[i][0], lng: data[i][1]},
          icon: {
           url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
            //url: "./static/Button_Icon_Green.svg.png"
          },
          map: map,
          draggable: false
       });
       
       let currDate = new Date();
       let date = new Date(data[i][2]);
       let diffe = diff_minutes(currDate, date); // Note: in minutes
       console.log("time difference: " + diffe + ' minutes');

       let density = parseInt(data[i][3]);
       let density_val;
       console.log("density: " + density);
       // Refer to this python file: density.py for these measurements 
       if(density<=4199){
        density_val = 0;
       }
       else if(density<=8938 && density>4199){
        density_val = 1;
        markerA.icon.url = "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png"
       }
       else if (density> 8938 && density<=32459){
        density_val = 2;
        markerA.icon.url = "http://maps.google.com/mapfiles/ms/icons/purple-dot.png"
       }
       else{
        // NOTE, IN 5 MINUTES THIS SHOULD DISAPPEAR AS PARKING WILL BE TAKEN FAST
        density_val = 5;
        markerA.icon.url = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
       }

       /* Comment out for now, re-work the time_risk and density data  */

       
       let time_risk = 0;
       if(diffe >5 && diffe<10){
        time_risk = 1;
       }
       if(diffe<10 && diffe>=5 ){
        time_risk = 1.5;
       }
       else if(diffe>=10 && diffe<13){
        time_risk = 2;
       }
       else if(diffe>=13 && diffe<16){
        time_risk = 3;
       }
       else if(diffe>=16 && diffe<20){
        time_risk = 5;
       }
       // Note, it's rare for parking space to stay for 20 minutes in NYC! After 20 minute the data should be GONE
       else if(diffe>=20){
        //markerA.setMap(null); # don't need if deleted 
        let entry = JSON.stringify(markerA.position.toJSON(), null, 2);
        // DELETE DATA 
        fetch ('/delete_data', {
          method : "POST",
          credentials : 'include',
          body : JSON.stringify(entry),
          cache : "no-cache",
          headers : new Headers ({
            "content-type" :"application/json"
         })
       }).then(() => location.reload()) // NOTE A POTENTIAL ISSUE: IF THERES LOTS OF PEOPLE AND THOUSANDS AND THOUSANDS OF TAGS THAN IT MIGHT JUST REFRESH EVERY SECOND OR SO
       }


       let combined_risk = time_risk + density_val;
       //console.log(combined_risk);

       if(combined_risk>5){
        //console.log("delete");
        //markerA.setMap(null);

        //DELETE DATA
        let entry = JSON.stringify(markerA.position.toJSON(), null, 2);
        fetch ('/delete_data', {
          method : "POST",
          credentials : 'include',
          body : JSON.stringify(entry),
          cache : "no-cache",
          headers : new Headers ({
            "content-type" :"application/json"
         })
       })
       } 

       let time = date.toLocaleTimeString();
       console.log(time);
       var infowindow = new google.maps.InfoWindow({
        content: "<p style='color: black; font-size: 20px'> Parking Spot Available  <br> Time Posted: " + time +" <br> " + diff_minutes(currDate, date) +  " minutes ago <br> Double click if the spot has been taken or if you took it!</p> <br> <img src='static/ParkingIcon.png' style='width: 100px; height: 100px'></img>"
       });
       
       markerA.addListener('mouseover', function() {
        infowindow.open(map, markerA);
       });

       markerA.addListener('mouseout', function() {
        infowindow.close();
       });


       google.maps.event.addListener(markerA,'dblclick', function(event){
        markerA.setMap(null);
        let entry = JSON.stringify(event.latLng.toJSON(), null, 2)
        console.log(entry)
        
        fetch ('/delete_data', {
          method : "POST",
          credentials : 'include',
          body : JSON.stringify(entry),
          cache : "no-cache",
          headers : new Headers ({
            "content-type" :"application/json"
         })
       })
     });
       
      
    }
    
})   
function diff_minutes(dt2, dt1) 
 {

  var diff =(dt2.getTime() - dt1.getTime()) / 1000;
  diff /= 60;
  return Math.abs(Math.round(diff));

 }