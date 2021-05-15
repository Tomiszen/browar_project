# Generated by Django 3.1.4 on 2021-01-03 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_distribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distribution',
            name='beer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beer_distribution', to='orders.beer'),
        ),
    ]
