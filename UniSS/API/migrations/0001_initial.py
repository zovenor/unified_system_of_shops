# Generated by Django 4.0.3 on 2022-03-15 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('key', models.CharField(default='BKneSqb5pRTidRzytvE2piBdBrKON12n', editable=False, max_length=32, unique=True)),
            ],
        ),
    ]
