# Generated by Django 3.0.1 on 2019-12-27 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0002_auto_20191224_0007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('director', models.CharField(max_length=255)),
                ('release_date', models.IntegerField()),
                ('duration', models.DurationField()),
                ('description', models.TextField(null=True)),
                ('link', models.CharField(max_length=255, null=True)),
                ('thumbnail', models.CharField(max_length=255, null=True)),
                ('trailer', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.RenameModel(
            old_name='Clients',
            new_name='Client',
        ),
        migrations.RenameModel(
            old_name='Seats',
            new_name='Seat',
        ),
        migrations.RenameModel(
            old_name='TicketTypes',
            new_name='TicketType',
        ),
        migrations.AddField(
            model_name='showtime',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='showtime',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.DeleteModel(
            name='Reservations',
        ),
        migrations.AddField(
            model_name='reservation',
            name='showtime_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worker.Showtime'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='ticket_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worker.Ticket'),
        ),
        migrations.AlterField(
            model_name='showtime',
            name='movie_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worker.Movie'),
        ),
        migrations.DeleteModel(
            name='Movies',
        ),
    ]