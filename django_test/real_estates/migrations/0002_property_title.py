# Generated by Django 4.0.9 on 2023-03-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='title',
            field=models.CharField(default='', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
