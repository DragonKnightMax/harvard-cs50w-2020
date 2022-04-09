# Generated by Django 3.1 on 2020-09-17 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_closebid_comment_listing_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='time',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='time',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='time',
        ),
        migrations.AddField(
            model_name='bid',
            name='date_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='date_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='date_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='closebid',
            name='win_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
