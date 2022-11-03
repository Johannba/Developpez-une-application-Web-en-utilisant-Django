from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=5000)
    image = models.ImageField()
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("posts")


class Review(models.Model):
    ticket = models.ForeignKey(blank=True, to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note"
    )
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(null=True, blank=True, verbose_name="Commentaire")
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0
    )
    time_created = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def get_absolute_url(self):
        return reverse("posts")
