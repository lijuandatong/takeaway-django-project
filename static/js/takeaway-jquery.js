$(document).ready(function () {
    //index rating
    $('.input-rating').rating({
        displayOnly: true,
        showCaption: false,
        showCaptionAsTitle: true,
        starCaptions: function (val) {
            return val + ' out of 5';
        }
    });

    initMap();

});


function initMap() {
// Create a new map object

    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 40.7128, lng: -74.0060 },
        zoom: 8,
    });

    // Retrieve location data from your database
    const address = $('#product_page').attr('data-address');

    // Geocode the address to get the latitude and longitude
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: address }, function(results, status) {
        if (status === "OK") {
            // Get the latitude and longitude
            const location = results[0].geometry.location;

            // Add a marker to the map at the desired location
            const marker = new google.maps.Marker({
                position: location,
                map: map,
                title: address,
            });

            // Set the map center to the marker position
            map.setCenter(location);
        } else {
            // Handle the geocoding error
            console.log("Geocode was not successful for the following reason: " + status);
        }
    });
}




document.addEventListener("DOMContentLoaded", function() {
    const minusButton = document.querySelector(".quantity-left-minus");
    const plusButton = document.querySelector(".quantity-right-plus");
    const inputField = document.querySelector("#quantity");

    minusButton.addEventListener("click", function() {
      let currentValue = parseInt(inputField.value);
      if (currentValue > 1) {
        inputField.value = (currentValue - 1).toString();
      }
    });

    plusButton.addEventListener("click", function() {
      let currentValue = parseInt(inputField.value);
      if (currentValue < 100) {
        inputField.value = (currentValue + 1).toString();
      }
    });
  });

  const button = document.querySelector('.add_cart .buy-now');
  button.addEventListener('click', function(event) {
      event.preventDefault();
      // Add item to cart
  });
