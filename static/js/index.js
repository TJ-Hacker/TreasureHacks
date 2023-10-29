
setTimeout(function(){
  document.querySelector(".preloader").style.display = "none";
}, 1000);

if (!sessionStorage.getItem('page_reloaded')) {
  sessionStorage.setItem('page_reloaded', true);
  location.reload();
}

let map, infoWindow;
// Create info


function initMap() {

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.650002, lng: -73.949997 },
    zoom: 15,
    disableDefaultUI: true,
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

// TEST FOR ME

let x;
// Fetch from the python file (check /data)
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
       let diffe = diff_minutes(currDate, date);
       console.log("time difference" + diffe);

       let density = parseInt(data[i][3]);
       let density_val;
       console.log("density" + density);
       if(density<=500){
        density_val = 0;
       }
       else if(density<=10000){
        density_val = 1;
       }
       else{
        density_val = 2;
        markerA.icon.url = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
       }
       let time_risk = 0;
       if(diffe>20){
        time_risk = 1;
       }
       let combined_risk = time_risk + density_val;
       //console.log(combined_risk);

       if(density_val == 1 && time_risk == 1){
        markerA.icon.url = "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png"
       }
       if(combined_risk>=4){
        //console.log("delete");
        markerA.setMap(null);
        let entry = JSON.stringify(markerA.position.toJSON(), null, 2);
        
       }
       let time = date.toLocaleTimeString();
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