import uuid

from crum import get_current_user
from django.db import models

from django_test.users.models import User
from .contanst import (AVAILABLE, PROPERTY_STATUS)


# Create your models here.
class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Updated at')
    updated_by = models.ForeignKey(User, editable=False, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="%(app_label)s_%(class)s_updated_by", verbose_name=u'Updated By')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Created at')

    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="%(app_label)s_%(class)s_created_by", verbose_name='Created By')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if self._state.adding:
            if isinstance(user, User):
                self.created_by = user
                self.updated_by = user
        else:
            self.updated_by = user
        super(BaseModel, self).save(*args, **kwargs)


class Property(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True, null=False)
    address = models.CharField(max_length=500)
    price = models.FloatField(default=0.0)
    is_lease = models.BooleanField(default=False)  # sale or lease
    is_suburb = models.BooleanField(default=False)  # suburb or in city
    status = models.CharField(choices=PROPERTY_STATUS, default=AVAILABLE, max_length=10)

    class Meta:
        db_table = 'property_res'
