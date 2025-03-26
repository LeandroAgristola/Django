function iniciarMap() {
    const map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -34.6037, lng: -58.3816 },
        zoom: 12
    });
}