# Generated by Django 3.1.7 on 2021-03-22 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210322_1327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registation',
            old_name='name',
            new_name='username',
        ),
    ]
