from django.db import models


class PropertyType(models.IntegerChoices):
    SALE = 0
    LEASE = 1


class PropertyStatus(models.IntegerChoices):
    AVAILABLE = 0
    SOLD = 1
    LEASED = 2
    DELETED = 3
