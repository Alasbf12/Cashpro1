# Generated by Django 3.0.2 on 2020-02-17 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ligdi', '0020_retour_ret_date_max'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versement',
            name='vers_tel',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
