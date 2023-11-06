from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    reason = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="Other")
    date = models.DateTimeField(auto_now_add=True)

class MoneyRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Request from {self.requester.username} - ${self.amount}"