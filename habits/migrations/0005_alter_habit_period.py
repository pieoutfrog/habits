# Generated by Django 4.2.8 on 2023-12-12 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_rename_associated_habit_habit_connected_habit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='period',
            field=models.IntegerField(default=1, verbose_name='Периодичность привычки'),
        ),
    ]
