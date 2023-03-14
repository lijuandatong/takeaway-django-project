from django.urls import path
from takeaway import views

app_name = "takeaway"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("account/<username>/", views.AccountView.as_view(), name="account"),
    path("charge/", views.ChargeView.as_view(), name="charge"),
    path("addCart/", views.AddCartView.as_view(), name="addCart"),
    path("takeaway/order_history.html", views.user_order_history, name="order_history"),
    path("product/", views.product, name="product"),
    path("cart/", views.user_cart, name="cart"),
    path("checkout/", views.user_checkout, name="checkout"),
]
