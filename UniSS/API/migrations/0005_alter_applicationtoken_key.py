# Generated by Django 4.0.3 on 2022-03-18 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_alter_applicationtoken_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationtoken',
            name='key',
            field=models.CharField(default='u7jWWFrdG6XG1LRsGZGYXmHPQcSxiPZZ', editable=False, max_length=32, unique=True),
        ),
    ]
