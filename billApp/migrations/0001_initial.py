# Generated by Django 4.0.6 on 2023-03-18 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('bill_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('purchaser', models.CharField(max_length=100)),
                ('purchaser_num', models.CharField(default='', max_length=15)),
                ('purchaser_address', models.CharField(default='', max_length=200)),
                ('purchaser_city', models.CharField(default='', max_length=50)),
                ('total_amount', models.CharField(max_length=30)),
                ('disscount', models.CharField(default='0', max_length=15)),
                ('final_amount', models.CharField(default='0', max_length=15)),
                ('bill_time', models.DateTimeField()),
                ('bill_data', models.TextField(default=' ', max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='CoustomersData',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('c_name', models.CharField(max_length=50)),
                ('c_number', models.CharField(max_length=50)),
                ('c_address', models.CharField(max_length=100)),
                ('c_city', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('pcode', models.CharField(max_length=100, unique=True)),
                ('pprice', models.CharField(max_length=100)),
                ('pimg', models.FileField(default='', max_length=200, upload_to='itemImage/')),
            ],
        ),
    ]
