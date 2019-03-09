# Generated by Django 2.1.7 on 2019-03-09 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Spider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spider_id', models.CharField(max_length=50)),
                ('spider_detail_Common', models.CharField(max_length=1200)),
                ('spider_detail_All', models.TextField()),
                ('spider_time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taobao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taobao_name', models.CharField(max_length=100)),
                ('taobao_id', models.CharField(max_length=50)),
                ('taobao_url', models.CharField(max_length=256)),
                ('taobao_shop_name', models.CharField(max_length=100)),
                ('taobao_price_now', models.CharField(max_length=50)),
                ('taobao_time', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
