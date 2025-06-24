from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('itens', '0003_alter_item_bloco'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReivindicacaoItem',
        ),
    ]
