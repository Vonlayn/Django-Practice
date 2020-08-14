from django.shortcuts import render, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Attraction, Review
from django.db.models import Avg
from .tables import AttractionTable
from django_tables2 import RequestConfig


def index(request):
    attractions = Attraction.objects.all()
    query = request.GET.get("q")

    if query:
        attractions = attractions.filter(name__icontains=query.title())

    return render(request, 'index.html', {'attractions': attractions})


def top(request):
    table = AttractionTable(list(Attraction.objects.all()), template_name="django_tables2/bootstrap4.html")
    RequestConfig(request).configure(table)
    return render(request, "top.html", {'table': table})


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['title', 'content', 'rating']
    template_name = 'review_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.attraction = get_object_or_404(Attraction, id=self.kwargs['id'])
        return super().form_valid(form)


class UpdateReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['title', 'content', 'rating']
    template_name = 'review_form.html'

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.attraction = get_object_or_404(Attraction, id=self.get_object().attraction_id)
        return super().form_valid(form)


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False

    def get_success_url(self):
        attraction = self.object.attraction
        return reverse('reviews', kwargs={'attr_id': attraction.id})


def reviews(request, attr_id):
    current_attr = Attraction.objects.get(id=attr_id)
    reviews = current_attr.review_set.all()
    middle_rating = 0
    rating_percent = list()
    rating_count = list()
    if current_attr.review_set.all().count() != 0:
        for i in range(5):
            rating_count.append(current_attr.review_set.filter(rating=(i + 1)).count())
            percent = round((current_attr.review_set.filter(rating=(i+1)).count() * 100) / current_attr.review_set.all().count())
            rating_percent.append(percent)
        middle_rating = round(current_attr.review_set.all().aggregate(Avg('rating'))["rating__avg"], 1)

    is_rev_created = None
    if request.user.is_active:
        is_rev_created = reviews.filter(author=request.user)
    return render(request, 'reviews.html', {'reviews': reviews,
                                            'rating_count': rating_count,
                                            'middle_rating': middle_rating,
                                            'percentage': rating_percent,
                                            'cur_attraction': current_attr,
                                            'attraction_id': attr_id,
                                            'is_rev_created': is_rev_created})

