# Generated by Django 5.1 on 2024-08-16 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_remove_amenities_hotel_remove_location_hotel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amenities',
            name='hotels',
        ),
        migrations.RemoveField(
            model_name='location',
            name='hotels',
        ),
        migrations.AddField(
            model_name='hotelinformation',
            name='amenities',
            field=models.ManyToManyField(related_name='hotels', to='polls.amenities'),
        ),
        migrations.AddField(
            model_name='hotelinformation',
            name='locations',
            field=models.ManyToManyField(related_name='hotels', to='polls.location'),
        ),
    ]
