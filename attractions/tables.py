import django_tables2 as tables
from .models import Attraction
import itertools


class AttractionTable(tables.Table):
    counter = tables.Column("#", empty_values=(), orderable=False)
    name = tables.Column("Достопримечательность", linkify=True)
    middle_value = tables.Column("Средний рейтинг", order_by="-middle_value")
    review_number = tables.Column("Количество отзывов", order_by="-review_number")

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(self.page.start_index()))
        return next(self.row_counter)

    class Meta:
        model = Attraction
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "country", "middle_value")
        sequence = ("counter", "name", "country")

