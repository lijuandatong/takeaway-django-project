$(document).ready(function () {
    $('#btn_charge').click(function () {
        var amount = $('#id_amount').val();
        if(amount == ''){
            alert("You should input the amount!");
            return;
        }
        //把用户输入的cash写入到数据库
        var username = $(this).attr('data-username');

        $.get('/takeaway/charge',
              {'username': username, 'amount': amount},
              function(data) {
                  $('#id_cash').text('￡' + data);
              })

        // dismiss dialog
        $('#chargeModal').modal('hide')
    });

    $('#btn_review').click(function () {
        var review = $('#id_review').val();
        alert("我的评价是：" + review);
        if(review == ''){
            alert("You should input the review!");
            return;
        }
        //把用户输入的review写入到数据库
        var username = $(this).attr('data-username');
        //var food_name = $(this).attr('data-food');

        $.get('/takeaway/review',
              {'username': username, 'review': review},
              function(data) {
                  $('#id_review').text(data);
              })

        // dismiss dialog
        $('#reviewModal').modal('hide')
    });

    $('.add_cart').click(function () {
        //把food加入到数据库
        var username = $(this).attr('data-username');
        var food_id = $(this).attr('data-food');

         $.get('/takeaway/addCart',
              {'username': username, 'food_id': food_id, 'count': 1},
              function(data) {
                  $('#id_cart').html(`<span class="icon-shopping_cart"></span>[${data}]`);
              })

    });

    $('#checkout-form').click(function () {
            var first_name = $('#id_checkout_firstname').val();
            var last_name = $('#id_checkout_lastname').val();
            var address = $('#id_checkout_address').val();
            var city = $('#id_checkout_city').val();
            var zipcode = $('#id_checkout_postcode').val();
            var email = $('#id_checkout_email').val();
            var phone = $('#id_checkout_phone').val();

            $.get('/takeaway/checkout_save_data',
              {'first_name':first_name, 'last_name':last_name,
                'city':city,
              'zipcode':zipcode, 'email':email,
              'phone':phone},
              function(response) {
                if (response.success) {
                    alert('Order placed successfully!');
                } else {
                    alert('There was an error with your order. Please check the form and try again.');
                }
            })
        });



    
});



    
        

 
    
            

