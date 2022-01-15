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
                        icon: this.getIcon(false, points.rest[i]['id'])
                    }).bindPopup(points.rest[i]['city']).addTo(this.map);
                }

                L.marker([points.mine.latitude, points.mine.longitude], {
                    icon: this.getIcon(true, points.mine.id)
                }).bindPopup(points.mine.city).addTo(this.map);
            }).catch(error => (console.error(error)));
        },

        buildMap: function() {
            this.map = L.map('map').setView([20, 0], 2);
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(this.map);
        },

        getIcon: function(own, id) {

            const Icon = L.divIcon({
                html: `
            <svg
              width="24"
              height="40"
              viewBox="0 0 100 100"
              version="1.1"
              preserveAspectRatio="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M0 0 L50 100 L100 0 Z" fill="${own ? '#7A8BE7' : '#4fcd29'}"></path>
              <text x="25" y="50" font-family="Verdana" font-size="45" fill="black">${id}</text>
            </svg>`,
                className: "",
                iconSize: [24, 40],
                iconAnchor: [12, 40],
            });
        return Icon;
        }
    }
}

</script>


