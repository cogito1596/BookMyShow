# Generated by Django 5.1.4 on 2024-12-14 23:05

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('duration', models.DurationField()),
                ('language', models.CharField(choices=[('EN', 'English'), ('HI', 'Hindi'), ('TA', 'Tamil'), ('TE', 'Telugu'), ('KA', 'Kannada'), ('MA', 'Malayalam')], max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.region')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('features', models.ManyToManyField(to='bookmyshow.feature')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.region')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('row_number', models.PositiveIntegerField()),
                ('seat_number', models.PositiveIntegerField()),
                ('col_number', models.PositiveIntegerField()),
                ('seat_type', models.CharField(choices=[('VIP', 'VIP'), ('EXEC', 'Executive'), ('NORMAL', 'Normal'), ('RECL', 'Recliner')], max_length=6)),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.screen')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.location')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.movie')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.screen')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShowFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_applicable', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.feature')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.show')),
            ],
        ),
        migrations.AddField(
            model_name='show',
            name='feature',
            field=models.ManyToManyField(through='bookmyshow.ShowFeature', to='bookmyshow.feature'),
        ),
        migrations.CreateModel(
            name='ShowSeat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seat_status', models.CharField(choices=[('AVL', 'Available'), ('BOK', 'Booked'), ('BLK', 'Blocked'), ('RES', 'Reserved')], max_length=3)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.seat')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.show')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShowSeatType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seat_type', models.CharField(choices=[('VIP', 'VIP'), ('EXEC', 'Executive'), ('NORMAL', 'Normal'), ('RECL', 'Recliner')], max_length=6)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.show')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Theatre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.region')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='screen',
            name='theatre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.theatre'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket_number', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('PEN', 'Pending'), ('CON', 'Confirmed'), ('CAN', 'Cancelled'), ('REF', 'Refunded')], max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.show')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('PEN', 'Pending'), ('SUC', 'Success'), ('FAL', 'Failed')], max_length=3)),
                ('method', models.CharField(choices=[('CAS', 'Cash'), ('CAR', 'Card'), ('UPI', 'UPI'), ('NET', 'Netbanking'), ('WAL', 'Wallet')], max_length=3)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.ticket')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketSeat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('show_seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmyshow.showseat')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_seats', to='bookmyshow.ticket')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
