# Generated by Django 3.2.7 on 2022-06-11 21:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toy', '0002_load_eyes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='age',
        ),
        migrations.AddField(
            model_name='person',
            name='birth_date',
            field=models.DateField(default=datetime.date.today()),
            preserve_default=False,
        ),
    ]
