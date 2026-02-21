from django.urls import path
from .views import ApplyJobView, ViewApplicants,UpdateApplicationStatus,EmployerApplicationsView,CandidateApplicationView

urlpatterns = [
    path('apply/<int:job_id>/',ApplyJobView.as_view(), name='apply-job'),
    path('applicants/<int:job_id>/',ViewApplicants.as_view(), name='view-applicants'),
    path('update-status/<int:application_id>/',UpdateApplicationStatus.as_view(),name='update-application-status'),
    path('employer/applications/', EmployerApplicationsView.as_view()),
    path('candidate/my-applications/', CandidateApplicationView.as_view())

]