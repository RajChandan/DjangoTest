# Generated by Django 2.1.7 on 2019-12-15 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='pub_date',
        ),
    ]
