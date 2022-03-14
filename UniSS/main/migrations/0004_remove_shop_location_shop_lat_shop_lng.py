# Generated by Django 4.0.3 on 2022-03-14 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_shopchain_unique_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='location',
        ),
        migrations.AddField(
            model_name='shop',
            name='lat',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='lng',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
    ]
