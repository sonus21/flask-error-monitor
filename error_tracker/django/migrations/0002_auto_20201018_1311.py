# Generated by Django 3.1.2 on 2020-10-18 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django', '0001_initial'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='errormodel',
        #     name='notification_send',
        #     field=models.BooleanField(default=False),
        # ),
        # migrations.AddField(
        #     model_name='errormodel',
        #     name='ticket_raised',
        #     field=models.BooleanField(default=False),
        # ),
        migrations.AlterField(
            model_name='errormodel',
            name='request_data',
            field=models.JSONField(),
        ),
    ]
