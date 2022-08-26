# Generated by Django 3.1.4 on 2021-02-10 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210209_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='account_type',
            field=models.CharField(choices=[(None, '(Unknown)'), ('PR', 'Personal'), ('GI', 'Influencer'), ('LI', 'Lifestyle Influencer'), ('FI', 'Fashion Influencer'), ('TI', 'Travel Influencer'), ('BR', 'Brand'), ('AD', 'Admin'), ('CL', 'Celeb'), ('HI', 'Home Influencer')], default='PR', max_length=2),
        ),
    ]