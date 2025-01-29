from django.urls import path

from .views import CustomUserListView, CustomUserDetailView
from .views import DestinationListView,DestinationDetailView,TravelPlanListView,TravelPlanDetailView
from .views import ActivityListView,ActivityDetailView,CommentListView,CommentDetailView,LoginView,LogoutView


urlpatterns = [
    path("customuser/", CustomUserListView.as_view(), name="CustomUserListView"),
    path("customuser/<int:pk>", CustomUserDetailView.as_view(), name="CustomUserDetailView"),
    path("destination/", DestinationListView.as_view(), name="DestinationListView"),
    path("destination/<int:pk>", DestinationDetailView.as_view(), name="DestinationDetailView"),
    path("travelplan/", TravelPlanListView.as_view(), name="TravelPlanListView"),
    path("travelplan/<int:pk>", TravelPlanDetailView.as_view(), name="TravelPlanDetailView"),
    path("activity/", ActivityListView.as_view(), name="ActivityListView"),
    path("activity/<int:pk>", ActivityDetailView.as_view(), name="ActivityDetailView"),
    path("comment/", CommentListView.as_view(), name="CommentListView"),
    path("comment/<int:pk>", CommentDetailView.as_view(), name="CommentDetailView"),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
]