# Generated by Django 3.0.2 on 2020-02-16 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ligdi', '0009_position_pos_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='versement',
            name='vers_nom',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='versement',
            name='vers_compte',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='versement',
            name='vers_num',
            field=models.CharField(default=' ', max_length=100),
        ),
    ]
