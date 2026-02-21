Job Portal API (Django + DRF + JWT)
Overview
A role-based  Job  Portal  REST API  built using  Django REST Framework with JWT Authentication.
•	Employers can create and manage jobs
•	Candidates can apply and track application status
•	Secure APIs using Access & Refresh Tokens
•	Pagination enabled for better performance
________________________________________
Features  
Authentication
•	Custom User Model (Employer / Candidate)
•	JWT (Simple JWT)
•	Protected APIs using IsAuthenticated
Employer
•	Create, update, delete jobs
•	View applicants
•	Accept / Reject applications
Candidate
•	View jobs (Paginated)
•	Apply for jobs (Resume upload)
•	Track application status
________________________________________
Tech Stack
•	Python
•	Django
•	Django REST Framework
•	Simple JWT
•	SQLite
________________________________________
Main Endpoints

Authentication (JWT)
  Method	Endpoint	                Description
-  POST	   /api/token/	         Obtain Access & Refresh Token
-  POST	  /api/token/refresh/	     Refresh Access Token
________________________________________
User / Registration
  Method	Endpoint	                 Description
-  POST	   /register/	   Register new user (Employer / Candidate)
________________________________________
Jobs
  Method	               Endpoint	             Description	              Access
-  GET	                    /jobs/	        List all jobs (Paginated)	   Public / Auth
-  POST	                    /jobs/	           Create new job	           Employer only
-  GET	                  /jobs/<id>/	     Get single job details	            Auth
-  PUT	                  /jobs/<id>/	         Update job	                Owner Employer
- DELETE	              /jobs/<id>/	         Delete job	                Owner Employer
-  GET	                /employer/jobs/	      View employer’s own jobs	     Employer only
________________________________________
Applications
  Method	                  Endpoint	                Description	                       Access
- POST	                  /apply/<job_id>/	          Apply for a job	                Candidate only
-  GET	              /candidate/applications/	  View candidate’s own applications	    Candidate only
-  GET	              /employer/applications/	  View all applications for employer    Employer only
                                                            jobs	
-  GET	             /jobs/<job_id>/applicants/	  View applicants for specific job	    Owner Employer
- PATCH	               /applications/<id>/	        Accept / Reject application	        Owner Employer

________________________________________

Header for Protected APIs

All protected endpoints require:  Authorization: Bearer <access_token>
________________________________________
Flow Summary

Candidate Flow
- Register
- Login → Get JWT token
- View jobs
- Apply for job
- Track status

Employer Flow
- Register
- Login → Get JWT token
- Create job
- View applicants
- Accept / Reject application