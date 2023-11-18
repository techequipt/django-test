from django.test import TestCase
from django_test.properties.constants import (DELETED, AVAILABLE)
from django_test.properties.api.views import PropertyFilter
import pytest

@pytest.mark.usefixtures("db")
class FilteringTest(TestCase):
    def test_sql_conditional_clause_when_filter_with_price_range(self):
        min_price = '1000.0'
        max_price = '2000.0'
        prop_filter = PropertyFilter(
            data = {
                'min_price': min_price,
                'max_price': max_price,
            },
            queryset=None
        )
        filtered_queryset = prop_filter.qs

        self.assertTrue(
            f'WHERE ("properties_property"."price" >= {min_price} AND "properties_property"."price" <= {max_price})'
            in str(filtered_queryset.query)
        )
    
    def test_sql_conditional_clause_when_filter_with_price_range_exclude_deleted_status(self):
        min_price = '1000.0'
        max_price = '2000.0'
        prop_filter = PropertyFilter(
            data = {
                'min_price': min_price,
                'max_price': max_price,
            },
            queryset=None
        )
        filtered_queryset = prop_filter.qs.filter(status=DELETED)

        self.assertTrue(
            (f'WHERE ("properties_property"."price" >= {min_price} '
             f'AND "properties_property"."price" <= {max_price} '
             f'AND "properties_property"."status" = {DELETED})')
            in str(filtered_queryset.query)
        )

    def test_sql_conditional_clause_when_filter_deleted_status_only(self):
        prop_filter = PropertyFilter(
            data = {},
            queryset=None
        )
        filtered_queryset = prop_filter.qs.exclude(status=DELETED)

        self.assertTrue(
            f'WHERE NOT ("properties_property"."status" = {DELETED})'
            in str(filtered_queryset.query)
        )
    
    def test_sql_conditional_clause_when_filter_all_fields(self):
        min_price = '1000.0'
        max_price = '2000.0'
        address = 'test address'
        is_suburb = False
        is_sale = True
        status = AVAILABLE

        prop_filter = PropertyFilter(
            data = {
                'min_price': min_price,
                'max_price': max_price,
                'address': address,
                'is_suburb': is_suburb,
                'is_sale': is_sale,
                'status': status,
            },
            queryset=None
        )
        filtered_queryset = prop_filter.qs.exclude(status=DELETED)

        self.assertTrue(
            (f'WHERE ("properties_property"."address" = {address} '
             f'AND NOT "properties_property"."is_suburb" '
             f'AND "properties_property"."is_sale" '
             f'AND "properties_property"."status" = {AVAILABLE} '
             f'AND "properties_property"."price" >= {min_price} '
             f'AND "properties_property"."price" <= {max_price} '
             f'AND NOT ("properties_property"."status" = DELETED))')
            in str(filtered_queryset.query)
        )
