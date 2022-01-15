from django.db import models
from django.utils.translation import gettext_lazy as _

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
            return str(self.name)