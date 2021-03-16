# Generated by Django 3.1.7 on 2021-03-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('bank_name', models.TextField()),
                ('ifsc', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('branch', models.TextField()),
                ('address', models.TextField()),
                ('district', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'BankDetails',
            },
        ),
    ]
