# Generated by Django 4.2 on 2024-01-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todomodel',
            name='uuid',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]