# Generated by Django 3.0.6 on 2020-06-12 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsites', '0009_auto_20200609_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basesite',
            name='creatTime',
            field=models.DateTimeField(),
        ),
    ]