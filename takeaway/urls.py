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
    path("orderdetail/<order_id>/", views.OrderDetailsView.as_view(), name="orderdetail"),
    path("foodDetail/<food_id>", views.FoodDetail.as_view(), name="foodDetail"),
    path("checkout/<cart_id>", views.CheckoutView.as_view(), name="checkout"),
    path('placeOrder/', views.PlaceOrder.as_view(), name='placeOrder'),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("removeFoodFromCart", views.RemoveFoodFromCart.as_view(), name="removeFoodFromCart"),
    path("minusQuantityFromCart", views.MinusQuantityFromCart.as_view(), name="minusQuantityFromCart"),
    # path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    # path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
]
