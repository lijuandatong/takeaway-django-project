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


});