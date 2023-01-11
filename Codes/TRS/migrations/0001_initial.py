# Generated by Django 3.2 on 2021-11-29 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('adminID', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('adminPassword', models.CharField(max_length=20)),
                ('Balance', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BUS',
            fields=[
                ('location', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('price', models.IntegerField()),
                ('numBus', models.IntegerField()),
                ('numAvail', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CUSTOMERS',
            fields=[
                ('custName', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('custID', models.CharField(max_length=20, unique=True)),
                ('custPassword', models.CharField(max_length=20)),
                ('age', models.IntegerField(null=True)),
                ('sex', models.CharField(max_length=5, null=True)),
                ('Balance', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FLIGHTS',
            fields=[
                ('flightNum', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('price', models.IntegerField()),
                ('numSeats', models.IntegerField()),
                ('numAvail', models.IntegerField()),
                ('FromCity', models.CharField(max_length=50)),
                ('ArivCity', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HOTELS',
            fields=[
                ('location', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('price', models.IntegerField()),
                ('numRooms', models.IntegerField()),
                ('numAvail', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RESERVATIONS',
            fields=[
                ('custName', models.CharField(max_length=50)),
                ('resvType', models.IntegerField()),
                ('resvKey', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]