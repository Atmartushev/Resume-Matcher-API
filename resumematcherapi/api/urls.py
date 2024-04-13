from django.urls import path
from . import views

urlpatterns = [
    #User
    path('user', views.getAllUsers),
    path('user/id/<int:id>', views.getUser),
    path('user/email/<str:email>', views.getUserByEmail),
    path('user/add', views.addUser),

    #JOBS
    path('job/all/user/id/<int:user_id>', views.getAllJobsByUserId),
    path('job/add/user/', views.post_job_by_user_id, name='post_job_by_user_id'),
    path('job/delete/id/<int:job_id>', views.delete_job, name='delete_job'),

    #Candidates
    path('candidate/all/job/id/<int:job_id>',views.getAllCandidatesByJobId),
    path('candidate/score/job/<int:job_id>', views.add_candidate),

    #Rubric
    path('rubric/add/', views.post_rubric),
    path('rubric/<int:id>', views.get_rubric),
]