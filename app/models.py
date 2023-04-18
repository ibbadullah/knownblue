from django.db import models

# Model for contact us
class ContactUsModel(models.Model):
    full_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    message = models.TextField(max_length=2000,null=True,blank=True)
    send_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contactusmodel"
