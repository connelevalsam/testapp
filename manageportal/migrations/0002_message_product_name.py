# Generated by Django 2.2.1 on 2019-06-21 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageportal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='product_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
