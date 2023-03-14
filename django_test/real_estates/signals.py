from django.db.models.signals import pre_save
from django.dispatch import receiver

from django_test.real_estates.models import Property


# @receiver(pre_save, sender=Property)
# def my_callback(sender, instance, *args, **kwargs):
#     print('111111111111111111')
#     instance.created_by = "creeeeeeee"
#     instance.updated_by = "tessssss"
