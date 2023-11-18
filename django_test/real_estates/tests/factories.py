from typing import Any
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory
from dateutil import tz

from django_test.users.tests.factories import UserFactory
from ..models import Property


class PropertyFactory(DjangoModelFactory):
    class Meta:
        model = Property

    address = Faker('street_address')
    suburb = Faker('city')
    is_for_sale = Faker('boolean')
    is_for_lease = Faker('boolean')
    status = Faker('random_element', elements=[choice[0] for choice in Property.STATUS_CHOICES])
    price = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    created_by = SubFactory(UserFactory)
    created_at = Faker('date_time_this_decade', tzinfo=tz.gettz('Australia / Sydney'))

    @post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create:
            return
        self.updated_at = Faker('date_time_this_month', tzinfo=tz.gettz('Australia / Sydney'))
