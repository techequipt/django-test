from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [('properties', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_suburb',
            field=models.BooleanField(
                default=False,
                help_text="Designates property whether it's suburb",
            ),
        ),
    ]