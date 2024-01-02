"""Models for real estate"""
from django.db import models
from django_test.base.models import BaseModel


class Property(BaseModel):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('leased', 'Leased'),
        ('deleted', 'Deleted'),
    ]

    address = models.CharField(max_length=300)
    suburb = models.CharField(max_length=100)
    for_sale_or_lease = models.BooleanField(default=True)  # True for sale, False for lease
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.address} - {self.suburb} - {self.get_status_display()}"

    def get_status_display(self) -> str:
        return dict(self.STATUS_CHOICES)[self.status]
