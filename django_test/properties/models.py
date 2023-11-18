from typing import Any
import django.utils.timezone
from django.db import models
from crum import get_current_user

from .constants import (AVAILABLE, DELETED, PROPERTY_STATUS)

class Property(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    address = models.CharField(max_length=500)
    price = models.FloatField(default=0.0)
    is_sale = models.BooleanField(default=False)
    status = models.CharField(choices=PROPERTY_STATUS, default=AVAILABLE, max_length=10)
    created_by = models.CharField(max_length=500, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Created at')
    last_modified = models.DateTimeField(blank=True, null=True, editable=False)
    is_suburb = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if self._state.adding:
            self.created_by = current_user
        else:
            self.last_modified = django.utils.timezone.now()
        super(Property, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.status = DELETED
        self.last_modified = django.utils.timezone.now()
        super(Property, self).save(*args, **kwargs)

    class Meta:
        db_table = 'properties_property'