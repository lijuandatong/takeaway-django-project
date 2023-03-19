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

    })
});