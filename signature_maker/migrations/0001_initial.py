# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('html', models.TextField(max_length=1000)),
                ('components', django.contrib.postgres.fields.ArrayField(size=10, null=True, base_field=models.CharField(max_length=20, null=True, blank=True), blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
