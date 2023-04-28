# Generated by Django 4.1.4 on 2023-04-26 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_alter_user_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='item',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
        migrations.AlterModelTable(
            name='cart',
            table='Cart',
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.items')),
            ],
            options={
                'db_table': 'CartItem',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(through='apps.CartItem', to='apps.items'),
        ),
    ]
