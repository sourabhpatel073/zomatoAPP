# Generated by Django 4.2.4 on 2023-08-20 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zesty_app', '0004_order_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_id',
        ),
    ]
