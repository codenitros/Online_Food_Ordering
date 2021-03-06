# Generated by Django 2.1 on 2019-05-20 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('Delivery_no', models.IntegerField(primary_key=True, serialize=False)),
                ('Dname', models.CharField(max_length=20)),
                ('Drating', models.IntegerField(default=0)),
                ('contact', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'deliveries',
            },
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favourite', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Oid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('address', models.CharField(default='', max_length=250)),
                ('postal_code', models.CharField(default='', max_length=20)),
                ('city', models.CharField(default='', max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='food.Order')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pid', models.CharField(max_length=40)),
                ('mode', models.CharField(max_length=20)),
                ('NetPrice', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'payments',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=20)),
                ('recipe_description', models.CharField(max_length=20)),
                ('recipe_price', models.IntegerField(default=0)),
                ('recipe_image', models.ImageField(blank=True, upload_to='recipe_imgs')),
                ('category', models.CharField(default=' ', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('rating', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, upload_to='restoimgs')),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='restaurant_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Restaurant'),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='Cid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.UserProfile'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='food.Recipe'),
        ),
        migrations.AddField(
            model_name='offer',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='food.Restaurant'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='res_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Restaurant'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='favourite',
            unique_together={('user_name', 'res_name')},
        ),
    ]
