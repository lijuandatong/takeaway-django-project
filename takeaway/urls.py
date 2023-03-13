from django.urls import path
from takeaway import views

app_name = "takeaway"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("account/<username>/account.html", views.AccountView.as_view(), name="account"),
    path("takeaway/order_history.html", views.user_order_history, name="order_history"),
    path("takeaway/product/", views.product, name="product"),
]
