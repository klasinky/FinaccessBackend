# Generated by Django 3.2.3 on 2021-05-25 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tag_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='label',
            field=models.CharField(default='', max_length=255, verbose_name='Label'),
        ),
    ]
