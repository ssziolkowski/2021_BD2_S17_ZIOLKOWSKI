# Generated by Django 3.1.7 on 2021-05-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_auto_20210526_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='login',
            field=models.TextField(default='company', unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='password',
            field=models.TextField(default='password', unique=True),
        ),
    ]