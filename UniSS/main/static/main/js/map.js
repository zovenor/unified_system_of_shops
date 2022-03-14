mapboxgl.accessToken = MAPBOX_TOKEN;
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [-74.5, 40], // starting position [lng, lat]
    zoom: 9 // starting zoom
});

let lat = 0;
let lng = 0;

navigator.geolocation.getCurrentPosition(function (position) {
        var locationMarker = null;
        if (locationMarker) {
            return;
        }

        lat = position.coords["latitude"];
        lng = position.coords["longitude"]

    },
    function (error) {
        console.log("Error: ", error);
    },
    {
        enableHighAccuracy: true
    }
);