# Generated by Django 3.1.4 on 2021-01-31 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210110_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='stock',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='status',
            field=models.CharField(choices=[('dostępne', 'Dostępne'), ('ostatnie_sztuki', 'Ostatnie sztuki'), ('niedostępne', 'Niedostępne')], default='niedostępne', max_length=15),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='package',
            field=models.CharField(choices=[('butelka', 'Butelka'), ('keg', 'Keg')], default='butelka', max_length=7),
        ),
    ]