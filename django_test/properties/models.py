from django.db import models

from django.contrib.auth import get_user_model

from .choices import PropertyType, PropertyStatus

User = get_user_model()

class Property(models.Model):
    """
    Real estate properties
    """
    
    address = models.TextField()
    type = models.IntegerField(choices=PropertyType.choices)
    status = models.IntegerField(choices=PropertyStatus.choices)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="created_by"
    )
