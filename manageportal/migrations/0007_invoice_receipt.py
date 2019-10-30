# Generated by Django 2.2.5 on 2019-10-08 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageportal', '0006_auto_20191003_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_path', models.CharField(max_length=300)),
                ('message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manageportal.Message')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_path', models.CharField(max_length=300)),
                ('message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manageportal.Message')),
            ],
        ),
    ]
