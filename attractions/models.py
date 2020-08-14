from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.db.models import Avg


class Attraction (models.Model):
    name = models.CharField("Достопримечательность", max_length=255)
    country = models.CharField("Страна", max_length=255)
    info = models.CharField(max_length=1024)
    image_url = models.CharField(max_length=2083)

    def review_number(self):
        if self.review_set.all().count() != 0:
            return self.review_set.all().count()
        else:
            return 0

    def middle_value(self):
        if self.review_set.all().count() != 0:
            value = round(self.review_set.all().aggregate(Avg('rating'))["rating__avg"], 1)
            return value
        else:
            return 0

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reviews', kwargs={'attr_id': self.id})


class Review (models.Model):
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Текст")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    rating = models.IntegerField("Оценка", validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('reviews', kwargs={'attr_id': self.attraction.id})


