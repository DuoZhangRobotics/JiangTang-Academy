# Generated by Django 2.2.7 on 2019-12-11 15:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20191211_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 11, 15, 27, 29, 389731, tzinfo=utc), verbose_name='date published'),
        ),
    ]