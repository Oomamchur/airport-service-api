# Generated by Django 4.2.3 on 2023-07-18 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airport_service', '0002_flight_crew'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='airplane',
            options={'ordering': ['airplane_name']},
        ),
        migrations.AlterModelOptions(
            name='airplanetype',
            options={'ordering': ['airplane_type']},
        ),
        migrations.AlterModelOptions(
            name='airport',
            options={'ordering': ['airport_name']},
        ),
        migrations.AlterModelOptions(
            name='flight',
            options={'ordering': ['-departure_time']},
        ),
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['source']},
        ),
        migrations.RenameField(
            model_name='airplane',
            old_name='airplane_type',
            new_name='type',
        ),
    ]