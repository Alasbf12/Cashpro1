# Generated by Django 3.0.2 on 2020-02-16 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ligdi', '0011_auto_20200216_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='versement',
            name='vers_tel',
            field=models.IntegerField(default=0),
        ),
    ]
