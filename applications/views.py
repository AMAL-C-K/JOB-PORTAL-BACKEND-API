from .serializers import ApplicationSerializer,ApplicationStatusUpdateSerializer
from .models import Application
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from job.models import Job
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination


# view for apply job

class ApplyJobView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # needed for resume upload

    def post(self, request, job_id):

        # check logged in user is candidate or not

        if request.user.role != 'candidate':   
            return Response({'error': 'Only candidates can apply'},status=status.HTTP_403_FORBIDDEN)

        try:
            job = Job.objects.get(id=job_id)  #check job exists or not 
        except Job.DoesNotExist:
            return Response({'error': 'job not found'},status=status.HTTP_404_NOT_FOUND)
        
        # check the candidate already applied or not

        if Application.objects.filter(job=job, candidate=request.user).exists(): 
            return Response({'error': 'you already applied for this job'},status=status.HTTP_400_BAD_REQUEST)

        serializer = ApplicationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(job=job, candidate=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# view for employer to check applications for a specific job

class ViewApplicants(APIView):

    def get(self ,request, job_id):
        if request.user.role != 'employer':  # check employer or not 
            return Response({'error':'Only employers can view applications'}, status=status.HTTP_403_FORBIDDEN)
        

        # Filter applications for that specific job if posted by the logged in employer

        applications = Application.objects.filter(job__id=job_id , job__employer = request.user)
        
        serializer = ApplicationSerializer(applications,many=True)

        return Response(serializer.data)


# view for update application status [accepted / rejected]

class UpdateApplicationStatus(APIView):

    permission_classes = [IsAuthenticated]

    # to change a field only - status
    def patch(self, request, application_id):

        # check employer or not
        if request.user.role != 'employer':   
            return Response({"error":"Only Employer can update status"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # get the application 
            application = Application.objects.get(id=application_id)
        
        except Application.DoesNotExist:
            return Response({"error":"Application Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        # check the job posted by logged in user or not
        if application.job.employer != request.user:
            return Response({"error":"You can only update your job applications"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ApplicationStatusUpdateSerializer(application, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view for the complete job applications get to a specific employer

class EmployerApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # check employer or not

        if request.user.role != 'employer':
            return Response({"error":"Only employer can view applications"}, status=status.HTTP_403_FORBIDDEN) 
        
        
        #filter all job applications for the specific employer
        applications = Application.objects.filter(job__employer=request.user).order_by('-applied_at')


        # paginator instance creation
        paginator = PageNumberPagination()

        # split queryset into  pages
        result_page = paginator.paginate_queryset(applications, request)

        # pass paginated data  to serializer 
        serializer = ApplicationSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    

# view for candidates to get all the applications submitted

class CandidateApplicationView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):

            # check candidate or not
        if request.user.role != 'candidate':

            return Response({"error":"Only candidates can view applications"}, status=status.HTTP_403_FORBIDDEN)

        # filter all applications submitted by the logged in candidate

        applications = Application.objects.filter(candidate=request.user).order_by('-applied_at')

        # paginator 
        
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(applications, request)

        serializer = ApplicationSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
