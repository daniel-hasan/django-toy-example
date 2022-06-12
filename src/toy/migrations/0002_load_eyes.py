from django.db import migrations
from django.core.management import call_command


def forwards_func(apps, schema_editor):
    call_command('loaddata', '../fixtures/eye_color.json', verbosity=2)


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('toy', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]