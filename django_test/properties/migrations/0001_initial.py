from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, 
                        max_length=255, 
                        verbose_name="Name of User"
                    ),
                ),
                (
                    "is_sale",
                    models.BooleanField(
                        default=False,
                        help_text="Designates property whether it's for sale or lease.",
                        verbose_name="sale or lease",
                    ),
                ),
                (
                    "price", 
                    models.FloatField(
                        default=0.0,
                        verbose_name="Price"
                    )
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ('AVAILABLE', 'Available'), 
                            ('SOLD', 'Sold'), 
                            ('LEASED', 'Leased'), 
                            ('DELETED', 'Deleted')
                        ], 
                        blank=True, 
                        max_length=10
                    )
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="When it was created"
                    ),
                ),
                (
                    "created_by",
                    models.CharField(
                        blank=True, 
                        max_length=255, 
                        verbose_name="The user who created it"
                    ),
                ),
                (
                    "last_modified",
                    models.DateTimeField(
                        blank=True, 
                        null=True, 
                        verbose_name="When it was last modified"
                    ),
                ),
            ],
            options={
                "verbose_name": "property",
                "verbose_name_plural": "property",
                "abstract": False,
            },
        ),
    ]
