from django.db import models

# Create your models here.


class BankDetails(models.Model):
    bank_name = models.TextField()
    ifsc = models.CharField(max_length=50, primary_key=True)
    branch = models.TextField()
    address = models.TextField()
    district = models.CharField(max_length=2501, default=True)
    state = models.CharField(max_length=250, default=True)
    city = models.CharField(max_length=250, default=True)
    phone = models.CharField(max_length=20, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "BankDetails"
