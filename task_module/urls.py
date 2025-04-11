from django.urls import path
from .views import Index_Page,Search_Tasks_By_Title,All_Tasks_List,Create_Task,Task_Details,Delete_Task,Filter_Tasks,Update_Subtasks,Delete_Subtasks

urlpatterns=[
    path('',Index_Page.as_view(),name='load_index'),
path('tasks/<title>',Search_Tasks_By_Title.as_view(),name='search_task_by_title'),
path('all_tasks/?order=<ordering>',All_Tasks_List.as_view(),name='all_tasks_list'),
path('create_task',Create_Task.as_view(),name='create_task'),
    path('task_details/<task_id>',Task_Details.as_view(),name='show_task_details'),
    path('delete_task/<task_id>',Delete_Task.as_view(),name='delete_task'),
path('update_subtasks/<task_id>',Update_Subtasks.as_view(),name='update_subtasks'),
    path('delete_subtasks',Delete_Subtasks.as_view(),name='delete_subtasks'),
    path('filter_tasks/<completion_percentage_minimum>/<deadline_min>/<deadline_max>',Filter_Tasks.as_view(),name='filter_tasks')
]