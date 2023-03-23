import django_filters
from .models import Apartment


class ApartmentFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')
    zipcode = django_filters.CharFilter()

    price = django_filters.RangeFilter()
    bedrooms = django_filters.ChoiceFilter(choices=Apartment.BEDROOM_CHOICES)
    bathrooms = django_filters.ChoiceFilter(choices=Apartment.BATHROOM_CHOICES)

    move_in_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Apartment
        fields = [
            'address', 'city', 'state', 'zipcode', 'price', 'bedrooms', 'bathrooms', 'move_in_date', 'is_furnished',
            'has_parking', 'has_balcony', 'has_pool', 'has_gym', 'has_washing_machine', 'has_dryer', 'has_dishwasher',
            'has_air_conditioning', 'has_wifi', 'has_bbq_facilities', 'is_available', 'available_from',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['address'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Address'})
        self.filters['city'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'City'})
        self.filters['state'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'State'})
        self.filters['zipcode'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Zipcode'})
        self.filters['price'].field.widget.attrs.update({'class': 'form-control'})
        self.filters['bedrooms'].field.widget.attrs.update({'class': 'form-select'})
        self.filters['bathrooms'].field.widget.attrs.update({'class': 'form-select'})
        self.filters['move_in_date'].field.widget.attrs.update({'class': 'form-control', 'type': 'date'})
