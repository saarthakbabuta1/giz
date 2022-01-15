from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254)
    email = models.EmailField()
    mobile = models.IntegerField()
    message = models.TextField(max_length=5000)
    contact_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact"
        verbose_name = _("contact")
    
        def __str__(self):
            return str(self.name)