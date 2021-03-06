# Generated by Django 2.2.5 on 2019-10-03 16:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manageportal', '0005_auto_20190930_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='message',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='message',
        ),
        migrations.RemoveField(
            model_name='messageimages',
            name='uploaded_at',
        ),
        migrations.AddField(
            model_name='message',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Coupons',
        ),
        migrations.DeleteModel(
            name='FeatureProducts',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
    ]
