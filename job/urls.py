from django.urls import path
from .views import JobCreateView,JobDetailView

urlpatterns = [
    path('jobs/', JobCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:job_id>/', JobDetailView.as_view(),name='job-detail')
]