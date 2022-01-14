from django.urls import path
from .views import OrdersViews,CancelOderView

app_name = 'orders'

urlpatterns = [
    path("",OrdersViews.as_view({'post':'post'},name="Add Orders")),
    path("<uuid:pk>",OrdersViews.as_view({'get':'retrieve'},name="Get Vendor")),
    path("cancel/<uuid:pk>",CancelOderView.as_view({'put':'put'},name = "Cancel Order"))
 ]

