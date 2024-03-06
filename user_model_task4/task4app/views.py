from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger('mylogger')
@api_view(http_method_names=['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ctreate_task(request):
    if request.method=='POST':
        try:
            serializer= TaskSerializer(data=request.data,context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Task created successfully...')
            return Response(data=serializer.data,status=201)
        except Exception as e:
            logger.error('error to create task..')
            return Response(data=serializer.errors,status=404)
        
    if request.method=='GET':
        try:
            obj=Task.objects.all()
            serializer=TaskSerializer(obj,many=True)
            logger.info('Tasks fetch successfully...')
            return Response(serializer.data,status=200)
        except:
            logger.error('error to fetch Task..')
            return Response(serializer.errors,status=405)
@api_view(http_method_names=['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def details_api(request,pk):
    obj= get_object_or_404(Task,pk=pk)
    if request.method=='GET':
        try:
            serializer=TaskSerializer(obj)
            logger.info('Task fetch successfully...')
            return Response(data=serializer.data,status=200)
        except:
            logger.error('error to fetching task')
            return Response(data={'details':'not found'},status=404)
    if request.method=='PUT':
        try:
            serializer=TaskSerializer(data=request.data,instanc=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Task updated successfully...')
            return Response(data=serializer.data,status=205)
        except:
            logger.error('Error to update the task..')
            return Response(serializer.errors,status=404)
    if request.method=='PATCH':
        try:
            serializer=TaskSerializer(data=request.data,instance=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('data partially update successfully..')
            return Response(data=serializer.data,status=204)
        except:
            logger.error('Error to task update partially.. ')
            return Response(data=serializer.errors,status=400)
    if request.method=='DELETE':
        try:
            obj.delete()
            logger.info('Task value is deleted..')
            return Response(data=None,status=204)
        except:
            logger.error('Error to delete the task..')
            return Response(data={'details':'Not Found'},status=404)
    
    
    

