# Generated by Django 3.1.4 on 2021-02-10 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainposts', '0005_auto_20210210_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpost',
            name='category',
            field=models.CharField(blank=True, choices=[('OTD', 'OOTD'), ('SEO', 'Special Event Outfit'), ('HOM', 'Home'), ('BAG', 'Bag'), ('BSH', 'Bookshelf'), ('TLD', 'Travel Diaries'), ('RSP', 'Restaurant Picks'), ('MFG', 'Favorite Gadgets'), ('MFA', 'Favorite Apps'), ('MFM', 'Favorite Movies'), ('SCR', 'Skincare Routine')], default='OTD', max_length=3),
        ),
    ]
