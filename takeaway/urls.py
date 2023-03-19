from django.urls import path
from takeaway import views

app_name = "takeaway"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("account/<username>/", views.AccountView.as_view(), name="account"),
    path("order_history/<username>/", views.OrderView.as_view(), name="order_history"),
    path("charge/", views.ChargeView.as_view(), name="charge"),
    path("review/", views.ReviewView.as_view(), name="review"),
    path("addCart/", views.AddCartView.as_view(), name="addCart"),
    # path("review/", views.user_order_review, name="review"),
    path("orderdetail/<order_id>/", views.OrderDetailsView.as_view(), name="orderdetail"),
    # path('addComment', views.AddComment.as_view(), name='addComment'),
    # path('addComment', views.AddComment, name='addComment'),
    path("product/", views.product, name="product"),
    path("cart/", views.user_cart, name="cart"),
    path("checkout/", views.user_checkout, name="checkout"),
]
