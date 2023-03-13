from django.urls import path
from takeaway import views

app_name = "takeaway"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("account/<username>/", views.AccountView.as_view(), name="account"),
    path("charge/", views.ChargeView.as_view(), name="charge"),
    path("product/", views.product, name="product"),
]
