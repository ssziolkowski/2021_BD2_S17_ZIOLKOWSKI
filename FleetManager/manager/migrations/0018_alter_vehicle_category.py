# Generated by Django 3.2.3 on 2021-06-04 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0017_auto_20210604_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='category',
            field=models.TextField(choices=[('sedan', 'sedan'), ('wagon', 'wagon'), ('hatchback', 'hatchback'), ('van', 'van'), ('pickup', 'pickup'), ('truck', 'truck'), ('construction', 'construction'), ('agriculture', 'agriculture'), ('storage', 'storage'), ('other', 'other')]),
        ),
    ]