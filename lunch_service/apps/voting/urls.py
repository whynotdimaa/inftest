from django.urls import path

from .views import TodayResultsView, VoteView

urlpatterns = [
    path("", VoteView.as_view(), name="vote"),
    path("results/today/", TodayResultsView.as_view(), name="results-today"),
]
