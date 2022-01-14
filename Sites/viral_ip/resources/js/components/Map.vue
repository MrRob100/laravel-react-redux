<template>
    <div class="contain">
        <div id="map">
        </div>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            map: {},
        };
    },

    mounted() {
        this.buildMap();

        this.addPointsToMap();
    },

    methods: {
        addPointsToMap: function() {
            axios.get("points").then(response => {
                let points = response.data;

                for (var i = 0; i < points.rest.length; i++) {
                    L.marker([points.rest[i]['latitude'], points.rest[i]['longitude']], {
                        icon: this.getIcon(false)
                    }).bindPopup(points.rest[i]['city']).addTo(this.map);
                }

                L.marker([points.mine.latitude, points.mine.longitude], {
                    icon: this.getIcon(true)
                }).bindPopup(points.mine.city).addTo(this.map);
            }).catch(error => (console.error(error)));
        },

        buildMap: function() {
            this.map = L.map('map').setView([20, 0], 2);
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(this.map);
        },

        getIcon: function(own) {
            let Icon = L.icon({
                iconUrl: own ? "icons/marker-red.png" : "icons/marker-blue.png",
                iconSize: [20, 20], // size of the icon
                shadowSize:   [50, 64], // size of the shadow
                iconAnchor: [10, 20], // point of the icon which will correspond to marker's location
                shadowAnchor: [4, 62],  // the same for the shadow
                popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
            });

        return Icon;
        }
    }
}

</script>


