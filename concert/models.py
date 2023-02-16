from django.db import models
from django.core.exceptions import ValidationError
from venue.models import Venue, SeatType

# Create your models here.
class Concert(models.Model):
    name = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    image = models.ImageField(null=True, default="concert.jpg")

    UTILIZATION_CHOICES = [(1, "1%"), (2, "2%"), (3, "3%"), (4, "4%"), (5, "5%"), (6, "6%"), (7, "7%"), (8, "8%"), (9, "9%"), (10, "10%"), (11, "11%"), (12, "12%"), (13, "13%"), (14, "14%"), (15, "15%"), (16, "16%"), (17, "17%"), (18, "18%"), (19, "19%"), (20, "20%"), (21, "21%"), (22, "22%"), (23, "23%"), (24, "24%"), (25, "25%"), (26, "26%"), (27, "27%"), (28, "28%"), (29, "29%"), (30, "30%"), (31, "31%"), (32, "32%"), (33, "33%"), (34, "34%"), (35, "35%"), (36, "36%"), (37, "37%"), (38, "38%"), (39, "39%"), (40, "40%"), (41, "41%"), (42, "42%"), (43, "43%"), (44, "44%"), (45, "45%"), (46, "46%"), (47, "47%"), (48, "48%"), (49, "49%"), (50, "50%"), (
        51, "51%"), (52, "52%"), (53, "53%"), (54, "54%"), (55, "55%"), (56, "56%"), (57, "57%"), (58, "58%"), (59, "59%"), (60, "60%"), (61, "61%"), (62, "62%"), (63, "63%"), (64, "64%"), (65, "65%"), (66, "66%"), (67, "67%"), (68, "68%"), (69, "69%"), (70, "70%"), (71, "71%"), (72, "72%"), (73, "73%"), (74, "74%"), (75, "75%"), (76, "76%"), (77, "77%"), (78, "78%"), (79, "79%"), (80, "80%"), (81, "81%"), (82, "82%"), (83, "83%"), (84, "84%"), (85, "85%"), (86, "86%"), (87, "87%"), (88, "88%"), (89, "89%"), (90, "90%"), (91, "91%"), (92, "92%"), (93, "93%"), (94, "94%"), (95, "95%"), (96, "96%"), (97, "97%"), (98, "98%"), (99, "99%"), (100, "100%")]
    seat_utilization = models.PositiveSmallIntegerField(choices=UTILIZATION_CHOICES, default=100)
    sold_seats = models.PositiveIntegerField(default=0)
    
    @property
    def total_seats(self):
        total = (int(self.venue.total_seats * (self.seat_utilization / 100)))
        return total


    @property
    def available_seats(self):
        seats = (self.total_seats - self.sold_seats)
        return seats

    def increase_sold_seats(self, quantity):
        self.sold_seats += quantity
        self.save()

        
    def __str__(self):
        return f"{self.name} - {self.venue.name}."

class ConcertTicket(models.Model):
    seat_type = models.ForeignKey(SeatType, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='seats')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        if self.seat_type.venue != self.concert.venue:
            raise ValidationError("Seat type must be from the same venue as the concert.")

    def __str__(self):
        return f"{self.concert} - {self.price}."
    
    def seats_left(self):
        left = self.concert.available_seats
        return left
    
