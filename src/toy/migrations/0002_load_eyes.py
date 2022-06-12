from django.db import migrations
from django.core.management import call_command


def add_eyes(apps, schema_editor):
    # Não é possivel importar a classe Pssoa diretamente já que a versão atual
    # pode ser mais nova que o migration necessitaria. 
    EyeColor = apps.get_model('toy', 'EyeColor')
    for eye,eye_human_read in EyeColor.color_name.field.choices:
        EyeColor.objects.create(color_name=eye)

class Migration(migrations.Migration):

    dependencies = [
        #ele deve ser executado após o 0001_initial
        ('toy', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_eyes),
    ]