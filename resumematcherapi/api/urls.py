from django.urls import path
from . import views

urlpatterns = [
    path('user', views.getAllUsers),
    path('user/id/<int:id>', views.getUser),
    path('user/email/<str:email>', views.getUserByEmail),
    path('user/add', views.addUser),

    #JOBS
    path('job/all/user/id/<int:user_id>', views.getAllJobsByUserId),


    #Candidates
    path('candidate/all/job/id/<int:job_id>',views.getAllCandidatesByJobId),
    
    path('candidate/score/job/<int:job_id>', views.add_candidate),
]