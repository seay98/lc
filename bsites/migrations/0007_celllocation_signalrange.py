# Generated by Django 3.0.6 on 2020-06-05 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsites', '0006_celllocation_coverage'),
    ]

    operations = [
        migrations.AddField(
            model_name='celllocation',
            name='signalrange',
            field=models.TextField(blank=True),
        ),
    ]