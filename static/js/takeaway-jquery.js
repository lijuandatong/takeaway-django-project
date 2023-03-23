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

    $('#id_points_checkbox').change(function () {
        var isChecked = $(this).is(':checked');
        if (isChecked) {
            var worth_cash = $(this).attr('data-equivalent-cash');
            var total_price = $(this).attr('data-total-price');
            var need_cash = parseFloat(total_price) - parseFloat(worth_cash);
            if (need_cash <= 0) {
                need_cash = 0;
            }
            $('#id_checkout_cash').html("<b>￡" + need_cash + "</b>");
        } else {
            $('#id_checkout_cash').html("<b>￡" + $(this).attr('data-total-price') + "</b>");
        }

        var wallet_cash = $('#wallet_cash').text().substring(1);
        if (wallet_cash >= need_cash) {
            $('#checkout-charge').hide();
            $('#checkout-form').prop('disabled', false);
        } else {
            $('#checkout-charge').show();
            $('#checkout-form').prop('disabled', true);
        }
    });

    initMap();
});

function initMap() {
// Create a new map object

    const map = new google.maps.Map(document.getElementById("map"), {
        center: {lat: 40.7128, lng: -74.0060},
        zoom: 8,
    });

    // Retrieve location data from your database
    const address = $('#product_page').attr('data-address');

    // Geocode the address to get the latitude and longitude
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({address: address}, function (results, status) {
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


document.addEventListener("DOMContentLoaded", function () {
    const minusButton = document.querySelector(".detail_minus");
    const plusButton = document.querySelector(".detail_plus");
    const inputField = document.querySelector("#quantity");

    minusButton.addEventListener("click", function () {
        let currentValue = parseInt(inputField.value);
        if (currentValue > 1) {
            inputField.value = (currentValue - 1).toString();
        }
    });

    plusButton.addEventListener("click", function () {
        let currentValue = parseInt(inputField.value);
        if (currentValue < 100) {
            inputField.value = (currentValue + 1).toString();
        }
    });
});

const button = document.querySelector('.add_cart .buy-now');
button.addEventListener('click', function (event) {
    event.preventDefault();
    // Add item to cart
});
