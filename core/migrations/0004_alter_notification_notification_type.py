# Generated by Django 3.2.3 on 2021-05-26 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_currency_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('post', 'post'), ('comment', 'comment'), ('follow', 'follow'), ('mention', 'mention')], max_length=20),
        ),
    ]