from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .mail import *
# Create your models here.

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name=_("Full Name"),max_length=254)
    email = models.EmailField()
    mobile = models.CharField(verbose_name=_("Mobile Number"),max_length=12)
    message = models.TextField(max_length=5000)
    contact_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact"
        verbose_name = _("contact")
    
        def __str__(self):
            return {"name":self.name,"email":self.email,"mobile":self.mobile,"message":self.message}

@receiver(post_save, sender=Contact)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        data = model_to_dict(instance)
        sender = "project.pvport@gmail.com"
        destination = "project.pvport@gmail.com"
        mail = send_mail(destination,sender,data["name"],data["mobile"],data["email"],data["message"])
        print(mail)
