from django.urls import path
from .views import ContactView

app_name = 'contact-us'

urlpatterns = [
    path("",ContactView.as_view({'get':'list'}),name="Contact-Us"),
    path("",ContactView.as_view({'post':'post'}),name="Add Contact-Us"), ]