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
        var id = $(this).attr('data-id');
        $(".cart_quantity").each(function(){
            if($(this).attr('data-id') == id){
                var cart_quantity = $(this).val();
                if (cart_quantity > 1) {
                    cart_quantity--;
                    $(this).val(cart_quantity);

                    var food_id = id;
                    $.get('/takeaway/minusQuantityFromCart',
                        {'food_id': food_id},
                        function (data) {
                            $('#id_cart').html(`<span class="icon-shopping_cart"></span>[${data}]`);
                        });
                }
            }
        });
    });

    $('.cart_plus').click(function () {
        var id = $(this).attr('data-id');
        $(".cart_quantity").each(function(){
            if($(this).attr('data-id') == id){
                var cart_quantity = $(this).val();
                cart_quantity++;
                $(this).val(cart_quantity);

                //把food加入到数据库
                var food_id = id;
                addFoodToCart(food_id, 1, function (data) {
                    $('#id_cart').html(`<span class="icon-shopping_cart"></span>[${data}]`);
                });
            }
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

    $('#id_points_checkbox').change(function () {
        var isChecked = $('#id_points_checkbox').is(':checked');
        if (isChecked) {
            alert("我被选中了");
            // 要修改
            $('#id_checkout_cash').html("<b>￡" + $(this).attr('data-total-price') + "</b>")
        } else {
            $('#id_checkout_cash').html("<b>￡" + $(this).attr('data-total-price') + "</b>")
        }
    });

    $('#checkout-form').click(function () {
        var order_id = $(this).attr('data-order-id');

        var first_name = $('#id_checkout_firstname').val();
        var last_name = $('#id_checkout_lastname').val();
        var address = $('#id_checkout_address').val();
        var city = $('#id_checkout_city').val();
        var zipcode = $('#id_checkout_postcode').val();
        var email = $('#id_checkout_email').val();
        var phone = $('#id_checkout_phone').val();

        var total_price = $('#id_points_checkbox').attr('data-total-price');
        var points = $('#id_points_checkbox').attr('data-points');

        var payment_points = 0;
        var payment_cash = 0;

        var isChecked = $('#id_points_checkbox').is(':checked');
        if (isChecked) {
            //用了积分
            payment_points = parseFloat(points);
            // 要修改
            var worth_cash = payment_points / 100;
            var float_total_price = parseFloat(total_price);
            payment_cash = 0;
            if (worth_cash >= float_total_price) {
                payment_cash = 0;
            } else {
                payment_cash = float_total_price - worth_cash;
            }
        } else {
            //未用积分
            payment_points = 0;
            // 要修改
            payment_cash = parseFloat(total_price);
        }

        alert('用了积分：' + payment_points + ",用了现金：" + payment_cash);

        $.get('/takeaway/placeOrder',
            {
                'first_name': first_name, 'last_name': last_name,
                'city': city, 'address': address,
                'zipcode': zipcode, 'email': email,
                'phone': phone,
                'payment_points': payment_points,
                'payment_cash': payment_cash,
                'order_id': order_id,
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





    
        

 
    
            

