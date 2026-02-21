from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer
from rest_framework.pagination import PageNumberPagination




# view for create job and view created jobs 
class JobCreateView(APIView):
    
    # access only for authenticated users

    permission_classes = [IsAuthenticated]

    # get all jobs 
    def get(self, request):

        jobs = Job.objects.all().order_by('-created_at')

        # pagination
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(jobs, request)

        serializer = JobSerializer(result_page, many=True)
        
        return Response(serializer.data)

    # for create job for employer
    def post(self, request):

            # check employer or not
        if request.user.role !='employer':

            return Response({"error":"Only Employers Can Create Jobs"}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(employer = request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view for update and delete a job by a employer
class JobDetailView(APIView):

    # check user is authenticated or not

    permission_classes = [IsAuthenticated]

    # to get the specific job object

    def get_object(self, job_id):
        try:
            return Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return None
        
       # update job 
    def put(self, request, job_id):

        job = self.get_object(job_id)

        if not job:
            return Response({"error":"Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #check the job posted by the logged in employer or not

        if job.employer != request.user:
            return Response({"error":"You can only update your jobs"}, status=status.HTTP_403_FORBIDDEN)
    
        serializer = JobSerializer(job,data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    # delete job
    def delete(self, request, job_id):

        job = self.get_object(job_id)
        
        if not job:
            return Response({"error":"job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #check the job posted by the logged in employer or not
        if job.employer != request.user:
            return Response({"error":"You can only delete your jobs"}, status=status.HTTP_403_FORBIDDEN)
        
        job.delete()
        return Response({"message":"jb deleted successfully"}, status=status.HTTP_204_NO_CONTENT)