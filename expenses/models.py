from django.db import models
from authentication.models import User


# Create your models here.
class Expense(models.Model):
    
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICE'),
        ('FOOD', 'FOOD'),
        ('TRAVEL', 'TRAVEL'),
        ('RENT', 'RENT'),
        ('OTHERS', 'OTHERS'),
    ]
    
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=255, null=True,)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null = False, blank = False)