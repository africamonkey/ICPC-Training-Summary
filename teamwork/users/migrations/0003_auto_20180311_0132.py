# Generated by Django 2.0.3 on 2018-03-11 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180310_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='team_member_1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='team_member_2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='team_member_3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='team_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
