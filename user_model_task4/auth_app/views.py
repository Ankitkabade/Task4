from django.shortcuts import render

from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
import logging
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .serializers import UserSerializer,User
from django.conf import settings
from task4app.utils import EmailThread
from task4app.tokens import account_activation_token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permission import IsOwnerIsAuthenticated
from .models import User







logger =logging.getLogger('mylogger')

@api_view(http_method_names=(['POST','GET']))
def user_api(request):
    if request.method=='POST':
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj=serializer.save()
            obj.is_active=False
            obj.save()
            
            domain = get_current_site(request=request).domain
            
            token =account_activation_token.make_token(obj)
            
            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            
            relative_url = reverse('activate',kwargs={'uid':uid,'token':token})
            
            absolute_url = f'http://%s'%(domain+relative_url,)
            
            message = "Hello %s,\n\t Thank you for creating account with us. Please click on the link below"\
            "to active your account\n %s"%(obj.username,absolute_url)
            subject="Account Activation Email"
            EmailThread(subject=subject,message=message,recipient_list=[obj.email],from_email=settings.EMAIL_HOST_USER).start()
            return Response({'Message':'please check your email for account activation mail'},status=201)
        except Exception as e:
            print(e)
            logger.error('error to creating  user')
            return Response(data=serializer.errors,status=404)
    if request.method =='GET':
        try:
            obj = User.objects.all()
            serializer= UserSerializer(obj,many = True)
            logger.info('Data Fetch successfully...')
            return Response(data=serializer.data,status=200)
        except Exception as e:
            
            logger.error('Error to fetch data')
            return Response(data=serializer.errors,status=404)
        

@api_view(http_method_names=('GET','POST','PUT','PATCH','DELETE'))
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerIsAuthenticated])
def details_api(request,pk):
    obj = get_object_or_404(User,pk=pk)
    if request.method == 'GET':
        try:
            serializer =UserSerializer(obj)
            logger.info('Data retrived successfully')
            return Response(data=serializer.data,status=201)
        except:
            logger.error('error for data retriving')
            return Response(data=serializer.data,status=401)
    if request.method=='PUT':
        try:
            serializer=UserSerializer(data=request.data,instance=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Data Updated Successfully...')
            return Response(data=serializer.data,status=202)
        except:
            logger.error('Error to update data')
            return Response(data=serializer.errors,status=204)
    if request.method=='PATCH':
        try:
            serializer=UserSerializer(data=request.data,instance=obj,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('data updated succefully..')
            return Response(data=serializer.data,status=207)
        except :
            logger.error('Error to update data...')
            return Response(data=serializer.errors,status=405)
    if request.method=='DELETE':
        try:
            obj.delete()
            logger.info('Record is deleted successfully..')
            return Response(data=None,status=206)
        except:
            logger.info('error to delete data')
            return Response(data={'details':'NOT Found'},status=407)
        

@api_view()       
def userAccountActivate(request,uid,token):

    if request.method=='GET':
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk= user_id)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist)as e:
            
            return Response(data={'details':'there is an error'},status=401)
        if account_activation_token.check_token(user=user,token=token):
            user.is_active=True
            user.save()
            return Response(data={'details':'Account Activated SuccessFully'},status=206)
        return Response(data={'details':'Account link Invalid'},status=400)