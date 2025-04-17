import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, F, ExpressionWrapper, FloatField, Q
from django.http import HttpRequest

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView
from rest_framework.authentication import SessionAuthentication,TokenAuthentication

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task,Sub_Task
from rest_framework.generics import ListAPIView
from .serializers import Task_Search_Serializer,Subtask_Update_Serializer
from .forms import Create_Task_Form,Create_Subtask_Form
from django.core.cache import cache
orders_dict={'creation_date_asc':'-creation_date','creation_date_des':'creation_date','deadline_asc':'-deadline','deadline_des':'deadline'
    ,'least_finished':'-unfinished'}


# Create your views here.
@method_decorator(login_required,name='dispatch')
class Index_Page(View):
    def get(self,request):
        unfinished_tasks=Task.objects.all().annotate(unfinished_count=Count('sub_tasks',filter=Q(sub_tasks__is_done=False))).\
        annotate(total=Count('sub_tasks')).order_by('-unfinished_count')[:1]

        recently_modified=Task.objects.\
        order_by('-last_modification_date')[:1].annotate(unf=Count('sub_tasks',filter=Q(sub_tasks__is_done=False))).annotate(total=Count('sub_tasks')).\
        annotate(unfinished=ExpressionWrapper(F('unf')*100/F('total'),output_field=FloatField()))


        return render(request,'Index.html',context={'recently_modified':recently_modified,'unfinished_tasks':unfinished_tasks})

class Search_Tasks_By_Title(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    queryset = Task.objects.all()
    serializer_class = Task_Search_Serializer
    def get_queryset(self):
        title=self.kwargs['title']
        user_id=self.request.user.id
        query_set=super().get_queryset().prefetch_related('sub_tasks').filter(creator_id=user_id,title__contains=title).annotate(
            unfinished=Count('sub_tasks',filter=Q(sub_tasks__is_done=False))).annotate(total=Count('sub_tasks')).annotate(
            completion_percentage=ExpressionWrapper(F('unfinished')*100/F('total'),output_field=FloatField())
        )
        print(query_set)
        return query_set


@method_decorator(login_required,name='dispatch')
class All_Tasks_List(ListView):
    model=Task
    template_name = 'My_Tasks.html'
    context_object_name = 'tasks'
    paginate_by = 25
    def get_queryset(self):
        query_set=super().get_queryset().prefetch_related('sub_tasks').all().values('title','creation_date')
        ordering=self.kwargs['ordering']
        try:
            order=orders_dict[ordering]
        except:
            order='?'
        self.ordering=order

        return query_set

@method_decorator(login_required,name='dispatch')
class Task_Details(ListView):
    template_name = 'Task_Details.html'
    model=Sub_Task
    context_object_name = 'sub_tasks'
    paginate_by = 25
    def get_queryset(self):
        task_id=self.kwargs['task_id']
        user=self.request.user
        query=Sub_Task.objects.all().filter(task_id=task_id,task__creator=user).select_related('task').order_by('is_done').all()
        try:
           self.task=query.first().task
        except:
            self.task=Task.objects.get(id=task_id,creator=user)
        return query
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        context['task']=self.task
        context['subtask_form']=Create_Subtask_Form(initial={'task':self.task})
        return context

@method_decorator(login_required,name='dispatch')
class Create_Task(View):
    def get(self,request):
        frm=Create_Task_Form()
        return render(request,'Create_Task.html',context={'creation_form':frm})
    def post(self,request):
        frm=Create_Task_Form(request.POST)
        if frm.is_valid():
            frm.instance.creator=request.user
            frm.save()
            return redirect(reverse('all_tasks_list'))
        else:
            return render(request,'Create_Task.html', context={'creation_form': frm})


@method_decorator(login_required,name='dispatch')
class Create_SubTask(View):
    def get(self,request):
        frm=Create_Task_Form()
        return render(request,'Create_SubTask.html',context={'subtask_form':frm})

    def post(self,request):
        subtask_form=Create_Subtask_Form(request.POST)
        if subtask_form.is_valid():
            if subtask_form.instance.task.creator==request.user:
                subtask_form.save()
                return redirect(reverse('all_tasks_list'))
            else:
                subtask_form.add_error('deadline','the parent of this subtask does not exist!')
                return render(request, 'Create_SubTask.html', context={'subtask_form': subtask_form})
        else:
            return render(request, 'Create_SubTask.html', context={'subtask_form': subtask_form})

@method_decorator(login_required,name='dispatch')
class Modify_Task(View):
    def post(self,request,task_id):
        try:
            with transaction.atomic():
              task=Task.objects.select_for_update().get(id=task_id,creator_id=request.user.id)
              frm=Create_Task_Form(request.POST,instance=task)
              if frm.is_valid():
                  frm.save()
                  return redirect(reverse('all_tasks_list', args=task.id))
              else:
                  return render(request, 'Modify_Task.html', context={'frm': frm})

        except Task.DoesNotExist:
            frm.add_error('description','task with such id was not found')
            return render(request,'Modify_Task.html', context={'frm': frm})

    def get(self,request,task_id):
        try:
            task=Task.objects.select_for_update().get(id=task_id,creator_id=request.user.id)
            frm=Create_Task_Form(instance=task)
            return render(request, 'Modify_Task.html', context={'frm': frm})
        except Task.DoesNotExist:
            return render(request, '404.html')

@method_decorator(login_required,name='dispatch')
class Delete_Subtasks(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def post(self,request):
        try:

            task_id=request.data['task_id']

            task=Task.objects.get(creator=request.user,id=task_id)
            ids=request.data['subtasks_ids'].split(',')
            print(ids,task_id)
            task.sub_tasks.filter(id__in=ids).delete()
            return Response(data={'message':'tasks were deleted successfully'},status=201)
        except Exception as exc:
            if isinstance(exc,json.JSONDecodeError):
                return Response(data={'message': 'improper json format!Make sure to edit your send your data like this:{task_id:your task_id,subtasks_ids:the ids'
                                                 'of the subtask you wish to delete} '}, status=400)
            elif isinstance(exc,Task.DoesNotExist):
                return Response(data={'message': 'task with such id was not found'}, status=404)
            else:

                return Response(data={'message': 'unknown error happend,pls try again'}, status=500)

@method_decorator(login_required,name='dispatch')
class Delete_Task(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    http_method_names = ['post']
    def post(self,request,task_id):
        try:
           Task.objects.get(id=task_id,creator=request.user).delete()
           return Response({'message':'Task was deleted successfully!'},status=201)
        except Exception as e:
            if isinstance(e,Task.DoesNotExist):
                return Response({'message': 'Task with such id was not found!,please,try again'}, status=404)
            else:
                return Response({'message':'Unkown error happend,pls try again!'},status=500)

@method_decorator(login_required,name='dispatch')
class Filter_Tasks(ListView):
    template_name = 'My_Tasks.html'
    model = Task
    context_object_name = 'tasks'
    paginate_by = 20
    def get_queryset(self):
        completion_percentage=self.kwargs['completion_percentage_minimum']
        deadline_min=self.kwargs['deadline_min']
        deadline_max=self.kwargs['deadline_max']

        condition=Q()
        if deadline_min!='__all__':
            min_date=datetime.datetime.strptime(deadline_min,'%Y-%m-%d').date()

            condition=condition & Q(deadline__gte=min_date)
        if deadline_max!='__all__':
            max_date = datetime.datetime.strptime(deadline_max, '%Y-%m-%d').date()
            condition = condition & Q(deadline__lte=max_date)
        if completion_percentage!='__all__':
            percentage=int(completion_percentage)
            query=super().get_queryset().filter(creator_id=self.request.user.id).annotate(finished=Count('sub_tasks',filter=Q(sub_tasks__is_done=True))).annotate(
                completion=ExpressionWrapper(F('finished')/Count('sub_tasks'),output_field=FloatField())
            ).filter(completion__gt=percentage)
            return query
        else:
            query=super().get_queryset().filter(Q(creator_id=self.request.user),condition)
            return query


class Update_Subtasks(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def post(self,request:HttpRequest,task_id):

        subtasks=request.data['result']
        try:
              task=Task.objects.get(id=task_id,creator=request.user)
              ids=subtasks.keys()
              query=task.sub_tasks.all().select_for_update().filter(id__in=ids)
              to_update=[]
              for tsk in query:
                  ser=Subtask_Update_Serializer(data=subtasks[str(tsk.id)])

                  if ser.is_valid():
                     tsk.title=ser.data['title']
                     tsk.deadline=ser.data['deadline']
                     tsk.is_done=ser.data['is_done']
                     tsk.description=ser.data['description']
                     to_update.append(tsk)
                  else:
                       return Response({'message':'could not update the given subtasks!check out the errors','errors':str(ser.errors)},status=400)
              Sub_Task.objects.bulk_update(to_update,fields=['title','deadline','is_done','description'])
              return Response({'message':'subtasks changed successfully!'},status=201)
        except Exception as e:
            if isinstance(e,Task.DoesNotExist):
                return Response({'message':'Task withc such id was not found!'},status=404)
            elif isinstance(e,json.JSONDecodeError):
                return Response({'message':'incorrect data format!make sure to enter your variables in this format:{result:{subtasks_id:{subtask title,subtask deadline,is done,description}}}'})
            else:
                return Response({'message':'an unkown error happend,please try again'},status=500)





