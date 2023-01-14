let map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.650002, lng: -73.949997 },
    zoom: 15,
  });
  infoWindow = new google.maps.InfoWindow();

  const locationButton = document.createElement("button");

  locationButton.textContent = "Switch to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
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
     console.log(JSON.stringify(event.latLng.toJSON(), null, 2)
     );
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
    for(i in data){
       console.log(data[i]);
    }
})
