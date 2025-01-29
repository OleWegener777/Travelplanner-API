from .models import CustomUser,Destination,TravelPlan,Activity,Comment
import django_filters.rest_framework as filters

SEX_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

COUNTRY_CHOICES = [
    ('T', 'Thailand'),
    ('I', 'Indonesia'),
    ('V', 'Vietnam'),
    ('M', 'Malaysia'),
    ('P', 'Philippines'),
    ('L', 'Laos'),
]


class CustomUserFilter(filters.FilterSet):
    dob_gte=filters.DateFilter(field_name="birthdate",lookup_expr="gte")
    dob_lte=filters.DateFilter(field_name="birthdate",lookup_expr="lte")
    sex=filters.TypedChoiceFilter(field_name="sex",choices=SEX_CHOICES)
    class Meta:
        model = CustomUser
        fields ={
            "username":["exact","contains","startswith"],
            "bio":["exact","contains","startswith"],
            "first_name":["exact","contains","startswith"]
        }


class DestinationFilter(filters.FilterSet):
    limit = filters.NumberFilter(method="limit_filter",label="Limit")
    user = filters.CharFilter(field_name="user__username",lookup_expr="contains")
    country =filters.TypedChoiceFilter(field_name="country",choices=COUNTRY_CHOICES)
    image_exists = filters.BooleanFilter(field_name="image", lookup_expr="isnull")    #->  needs to be fixed
    class Meta:
        model = Destination
        fields = {
            "name":["exact","contains","startswith"],
            "description":["exact","contains","startswith"],
            "best_time_to_visit":["exact","contains","startswith"],
            #"image": ["exact", "contains", "startswith"]
        }

    def limit_filter(self,queryset,name,value):
        return queryset[:value] if value else queryset
    
    
class TravelPlanFilter(filters.FilterSet):
    limit = filters.NumberFilter(method="limit_filter",label="Limit")
    user = filters.CharFilter(field_name="user__username",lookup_expr="contains")
    destinations = filters.CharFilter(field_name="destinations__name",lookup_expr="contains")
    traveldays_gte=filters.NumberFilter(field_name="traveldays",lookup_expr="gte")
    traveldays_lte=filters.NumberFilter(field_name="traveldays",lookup_expr="lte")
    class Meta:
        model = TravelPlan
        fields = {
            "title":["exact","contains","startswith"],
            "description":["exact","contains","startswith"]
        }

    def limit_filter(self,queryset,name,value):
        return queryset[:value]    
    
    
class ActivityFilter(filters.FilterSet):
    limit = filters.NumberFilter(method="limit_filter",label="Limit")
    destinations = filters.CharFilter(field_name="destinations__name",lookup_expr="contains")
    travel_plans = filters.CharFilter(field_name="travel_plans",lookup_expr="contains")
    class Meta:
        model = Activity
        fields = {
            "name":["exact","contains","startswith"]
        }

    def limit_filter(self,queryset,name,value):
        return queryset[:value]    
    
    
class CommentFilter(filters.FilterSet):
    limit = filters.NumberFilter(method="limit_filter",label="Limit")
    user = filters.CharFilter(field_name="user__username",lookup_expr="contains")
    destination = filters.CharFilter(field_name="destination__name",lookup_expr="contains")
    travel_plan = filters.CharFilter(field_name="travel_plan__title",lookup_expr="contains")
    class Meta:
        model = Comment
        fields = {
            "comment":["exact","contains","startswith"]
        }

    def limit_filter(self,queryset,name,value):
        return queryset[:value]            