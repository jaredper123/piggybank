from django.db import models

from django.db import models

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    reason = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="Other")
    date = models.DateTimeField(auto_now_add=True)

