var map;
$(function() {
    function Map(settings) {
        settings = settings || {};
        var canvasId = settings.canvasId || 'map-canvas';
        var mapOptions = settings.mapOptions || {
            zoom: 8,
            center: new google.maps.LatLng(-34.397, 150.644)
        };
        var localMap = null;
        var localMarker = null;

        function initialize() {
            localMap = new google.maps.Map(
                document.getElementById(canvasId),
                mapOptions
            );
            
            // A marker will be added after the map is clicked
            google.maps.event.addListener(localMap, 'click', function(e) {
                placeMarker(e.latLng);
            });
        }

        function placeMarker(position, lat, lng) {
            var pos = position || new google.maps.LatLng(lat, lng);
            var markerOptions = {
                position: pos,
                map: localMap,
                draggable: true
            };
            localMarker = new google.maps.Marker(markerOptions);
            localMap.setCenter(pos);
            return {lat: pos.lat(), lng: pos.lng()};
/*
            google.maps.event.addListener(marker, 'click', toggleBounceMarker);
            if (setSelected === true) {
                google.maps.event.trigger(marker, 'click');
            }
*/
        }

        function toggleBounceMarker() {
            console.log(marker);
            if (marker.getAnimation() != null) {
                marker.setAnimation(null);
            } else {
                marker.setAnimation(google.maps.Animation.BOUNCE);
            }
        }

        function removeMarker() {
            if (localMarker === null) {
                return;
            }
            google.maps.event.clearInstanceListeners(localMarker);
            localMarker.setMap(null);
            localMarker = null;
        }
        
        return {
            initialize: initialize,
            placeMarker: placeMarker,
            removeMarker: removeMarker
        };
    };

    map = Map();
    map.initialize();
});
