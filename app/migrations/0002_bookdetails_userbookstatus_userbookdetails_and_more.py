# Generated by Django 4.2.6 on 2023-12-02 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('book_code', models.IntegerField()),
                ('author_name', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=128)),
                ('amount', models.IntegerField()),
                ('available_books', models.IntegerField()),
                ('created_date', models.DateField()),
                ('created_by', models.IntegerField()),
                ('updated_date', models.DateField(null=True)),
                ('updated_by', models.IntegerField(null=True)),
                ('book_img', models.FileField(upload_to='image')),
            ],
        ),
        migrations.CreateModel(
            name='UserBookStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.bookdetails')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.studentdetails')),
            ],
        ),
        migrations.CreateModel(
            name='UserBookDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('books_quantity', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.studentdetails')),
            ],
        ),
        migrations.CreateModel(
            name='Booktransferhistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('book_name', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.studentdetails')),
            ],
        ),
    ]
