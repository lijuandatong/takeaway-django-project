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

    $('.add_cart').click(function () {
        //把food加入到数据库
        var username = $(this).attr('data-username');
        var food_id = $(this).attr('data-food');

         $.get('/takeaway/addCart',
              {'username': username, 'food_id': food_id, 'count': 1},
              function(data) {
                  $('#id_cart').html(`<span class="icon-shopping_cart"></span>[${data}]`);
              })

    })

    $('#checkout-form').click(function () {
          
            var first_name = $(this).attr('data-first_name');
            var last_name = $(this).attr('data-last_name');
            var address = $(this).attr(' data-address');
            var city = $(this).attr('data-city');
            var zipcode = $(this).attr('data-zipcode');
            var email = $(this).attr('data-email');
            var phone = $(this).attr('data-phone');


            $.get('/takeaway/checkout_save_data',
              {'first_name':first_name, 'last_name':last_name,
              'address':address, 'city':city,
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



    
        

 
    
            

