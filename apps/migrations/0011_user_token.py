# Generated by Django 4.1.4 on 2023-04-27 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_alter_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
