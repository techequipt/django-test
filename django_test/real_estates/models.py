from django.db.models import (
    Model,
    CharField,
    BooleanField,
    DecimalField,
    DateTimeField,
    ForeignKey,
    SET_NULL,
)
from django_test.users.models import User
from django.utils.translation import gettext_lazy as _

class Property(Model):
    STATUS_CHOICES = [
        ('available', _('Available')),
        ('sold', _('Sold')),
        ('leased', _('Leased')),
        ('deleted', _('Deleted')),
    ]

    address = CharField(_("Address"), max_length=255)
    suburb = CharField(_("Suburb"), max_length=255)  # Add a field for the property's suburb
    is_for_sale = BooleanField(_("For sale"), default=False)
    is_for_lease = BooleanField(_("For lease"), default=False)
    status = CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='available')
    price = DecimalField(_("Price"), max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = DateTimeField(_("Updated At"),auto_now=True)
    created_by = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.address} - {self.get_status_display()}"

    class Meta:
        db_table = 'real_estate_properties'
