# Generated by Django 4.1.4 on 2023-05-02 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0021_user_display_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
