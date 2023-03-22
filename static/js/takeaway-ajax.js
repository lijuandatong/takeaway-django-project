$(document).ready(function () {
    $('#btn_charge').click(function () {
        var amount = $('#id_amount').val();
        if (amount == '') {
            alert("You should input the amount!");
            return;
        }
        //把用户输入的cash写入到数据库
        var username = $(this).attr('data-username');

        $.get('/takeaway/charge',
            {'username': username, 'amount': amount},
            function (data) {
                $('#id_cash').text('￡' + data);
            })

        // dismiss dialog
        $('#chargeModal').modal('hide')
    });

    $('#btn_review').click(function () {
        var comment = $('#id_review').val();
        if (comment == '') {
            alert("You should input the review!");
            return;
        }
        //把用户输入的review写入到数据库
        var username = $(this).attr('data-username');
        var food = $(this).attr('data-food');
        if (food == '') {
            food = 'Tofu with Kung Po Sauce';
        }
        alert(comment + " " + username + " " + food)
        //var food_name = $(this).attr('data-food');

        $.get('/takeaway/review',
            {'review': comment, 'username': username, 'food': food},
            function (data) {

            })

        // dismiss dialog
        $('#reviewModal').modal('hide')
    });

    $('.add_cart').click(function () {
        //把food加入到数据库
        var food_id = $(this).attr('data-food');
        addFoodToCart(food_id, 1, function (data) {
            $('#id_cart').html(`<span class="icon-shopping_cart"></span>[${data}]`);
        });
    });

    $('.cart_minus').click(function () {
        //更新数据库
        var cart_quantity = $('.cart_quantity').val();
        if (cart_quantity > 1) {
            cart_quantity--;
            $('.cart_quantity').val(cart_quantity);
        }

        var food_id = $(this).attr('data-food');
        alert("减少数量" + food_id)

        $.get('/takeaway/minusQuantityFromCart',
              {'food_id': food_id},
              function(data) {
                  $('#id_cart').html(`<span class="icon-shopping_cart"></span>[${data}]`);
              });
    });

    $('.cart_plus').click(function () {
        var cart_quantity = $('.cart_quantity').val();
        cart_quantity++;
        $('.cart_quantity').val(cart_quantity);

        //把food加入到数据库
        var food_id = $(this).attr('data-food');
        addFoodToCart(food_id, 1, function (data) {
            $('#id_cart').html(`<span class="icon-shopping_cart"></span>[${data}]`);
        });
    });

    $('.product-remove').click(function () {
        var cart_detail_id = $(this).attr('data-product');

        $.get('/takeaway/removeFoodFromCart',
            {'cart_detail_id': cart_detail_id},
            function () {
                //刷新购物车页面

            })
    });

    $('#checkout-form').click(function () {

        var first_name = $(this).attr('data-first_name');
        var last_name = $(this).attr('data-last_name');

        var city = $(this).attr('data-city');
        var zipcode = $(this).attr('data-zipcode');
        var email = $(this).attr('data-email');
        var phone = $(this).attr('data-phone');


        $.get('/takeaway/checkout_save_data',
            {
                'first_name': first_name, 'last_name': last_name,
                'city': city,
                'zipcode': zipcode, 'email': email,
                'phone': phone
            },
            function (response) {
                if (response.success) {
                    alert('Order placed successfully!');
                } else {
                    alert('There was an error with your order. Please check the form and try again.');
                }
            })
    });

});

function addFoodToCart(food_id, count, callback) {
    $.get('/takeaway/addCart',
        {'food_id': food_id, 'count': count},
        callback);
}





    
        

 
    
            

