from django.urls import path
from . import views

urlpatterns = [
    #User
    path('user', views.getAllUsers),
    path('user/id/<int:id>', views.getUser),
    path('user/email/<str:email>', views.getUserByEmail),
    path('user/add', views.addUser),
    path('user/update/<int:id>', views.update_user),

    #JOBS
    path('job/all/user/id/<int:user_id>', views.getAllJobsByUserId),
    path('job/add/user/', views.post_job_by_user_id, name='post_job_by_user_id'),
    path('job/update/id/<int:job_id>', views.update_job),
    path('job/delete/id/<int:job_id>', views.delete_job, name='delete_job'),

    #Candidates
    path('candidate/all/job/id/<int:job_id>',views.getAllCandidatesByJobId),
    path('candidate/score/job/<int:job_id>/generaterubric', views.add_candidate_with_generated_rubric),
    path('candidate/score/job/<int:job_id>', views.add_candidate),
    path('candidate/update/<int:job_id>', views.update_candidate),
    path('candidate/delete/<int:job_id>', views.delete_candidate),

    #Rubric
    path('rubric/add/', views.post_rubric),
    path('rubric/<int:id>', views.get_rubric),
    path('rubric/update/<int:id>', views.update_rubric),
    path('rubric/delete/<int:id>', views.delete_rubric),
]