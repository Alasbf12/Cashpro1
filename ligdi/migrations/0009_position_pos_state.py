# Generated by Django 3.0.2 on 2020-02-15 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ligdi', '0008_auto_20200215_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='pos_state',
            field=models.BooleanField(default=False),
        ),
    ]
