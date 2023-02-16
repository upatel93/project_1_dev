from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    @property
    def total_seats(self):
        seats = sum(seat_type.num_seats for seat_type in self.seattype_set.all())
        return seats

    def __str__(self):
        return f'{self.name} - {self.location} - {self.total_seats}'

class SeatType(models.Model):
    SEAT_TYPE_LEVEL1 = 'L1'
    SEAT_TYPE_LEVEL2 = 'L2'
    SEAT_TYPE_LEVEL3 = 'L3'
    SEAT_TYPE_GOLD = 'GO'
    SEAT_TYPE_SILVER = 'SI'
    SEAT_TYPE_BRONZE = 'BR'

    SEAT_TYPE_CHOICES = [
        (SEAT_TYPE_LEVEL1, 'Level 1'),
        (SEAT_TYPE_LEVEL2, 'Level 2'),
        (SEAT_TYPE_LEVEL3, 'Level 3'),
        (SEAT_TYPE_GOLD, 'Gold'),
        (SEAT_TYPE_SILVER, 'Silver'),
        (SEAT_TYPE_BRONZE, 'Bronze'),
    ]

    type = models.CharField(
        max_length=100,
        choices=SEAT_TYPE_CHOICES,
        default=SEAT_TYPE_LEVEL1
    )
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    num_seats = models.PositiveIntegerField()

    def __str__(self):
        seat_type = None
        for choice in self.SEAT_TYPE_CHOICES:
            if choice[0] == self.type:
                seat_type = choice[1]
                break
        return f"{self.venue.name} - {seat_type}"

