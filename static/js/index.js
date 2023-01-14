if (!sessionStorage.getItem('page_reloaded')) {
  sessionStorage.setItem('page_reloaded', true);
  location.reload();
}
let map, infoWindow;

function initMap() {

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.650002, lng: -73.949997 },
    zoom: 15,
    disableDefaultUI: true,
    // fullscreenControl: false
  });
  infoWindow = new google.maps.InfoWindow();

  const locationButton = document.createElement("button");

  locationButton.textContent = "Center";
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
        draggable: true
     });
     google.maps.event.addListener(marker,'dblclick', function(event){
        marker.setMap(null);
        
     });
     //console.log(JSON.stringify(event.latLng.toJSON(), null, 2));
     let entry = JSON.stringify(event.latLng.toJSON(), null, 2);
     console.log(entry);

     fetch ('/add_data', {
      method : "POST",
      credentials : 'include',
      body : JSON.stringify(entry),
      cache : "no-cache",
      headers : new Headers ({
        "content-type" :"application/json"
     })
   }) 
    }) 
  
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

fetch('/data')
.then(response => response.json())
.then(data => {
    console.log(data);

    for(let i = 0; i < data.length; i++){
      
        let marker = new google.maps.Marker({
          position: {lat: data[i][0], lng: data[i][1]},
          icon: {
            // url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
            url: "./static/ParkingIcon.png"
          },
          map: map,
          draggable: false
       });
       
        
      
    }
    
})   
