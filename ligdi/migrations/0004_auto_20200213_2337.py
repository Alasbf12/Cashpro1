# Generated by Django 3.0.2 on 2020-02-13 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ligdi', '0003_auto_20200213_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id_picture',
            field=models.ImageField(upload_to='ligdi/static/ligdi/ids'),
        ),
    ]