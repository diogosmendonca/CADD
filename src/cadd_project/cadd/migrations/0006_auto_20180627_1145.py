# Generated by Django 2.0.6 on 2018-06-27 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadd', '0005_auto_20180624_1457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parametros',
            old_name='maxcreditosporperiodopreta',
            new_name='mincreditosporperiodopreta',
        ),
    ]