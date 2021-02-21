# Generated by Django 3.1.7 on 2021-02-20 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BakeryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.SlugField(unique=True)),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=1000)),
                ('Item_count_in_package', models.IntegerField(blank=True, null=True)),
                ('measurement_type', models.CharField(choices=[(1, 'Weight'), (2, 'Packaging')], default='', max_length=100)),
                ('weight', models.FloatField(blank=True, help_text='weight in grams', null=True)),
                ('type', models.CharField(choices=[(1, 'dry'), (2, 'wet')], default='', max_length=100)),
                ('price', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturing_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('quantity', models.IntegerField(default=0)),
                ('bakery_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bakery_item_inventory', to='api.bakeryitem')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientsWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(blank=True, help_text='weight in grams', null=True)),
                ('bakery_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_ratio', to='api.bakeryitem')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_ratios', to='api.ingredients')),
            ],
        ),
    ]
