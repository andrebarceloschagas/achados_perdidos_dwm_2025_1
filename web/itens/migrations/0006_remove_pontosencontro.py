from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('itens', '0005_merge_20250624_1012'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PontoEncontro',
        ),
    ]
