from ast import Not
import math, random
from django.conf import settings
from rest_framework.permissions import AllowAny
from .serializer import RegisterSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import LoginSerializer
from rest_framework.permissions import IsAdminUser
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
from django.contrib.auth.models import update_last_login
from  rest_framework.permissions import IsAuthenticated
from twilio.rest import Client 

class UserloginView(generics.CreateAPIView):
    permission_classes= (AllowAny,)
    serializer_class = LoginSerializer 

    # def post(self, request):
    #     user= request.data
    #     serializer= self.serializer_class(data = request.data)
    #     serializer.is_valid(raise_exception=True)
    #     if serializer.is_valid():
    #         if request.data.get('mobile_number'):
    #             mobile_number = request.data.get('mobile_number', None)
    #             try:
    #                 user= CustomUser.objects.get(mobile_number=mobile_number)
    #                 ses_var = user.id   
    #                 request.session['ses_var'] = ses_var
    #                 otpfromlogin = request.session['ses_var'] = ses_var
    #             except:
    #                 return Response({"error": "Your username/email is not correct. Please try again or register your details"})
    #             ######################################################### otp ####################################################
    #             digits = "0123456789"
    #             OTP = ""
    #             for i in range(4):
    #                 OTP += digits[math.floor(random.random() * 10)]
    #             Data = int(OTP)
    #             print("--------------------------------------->> OTP: ", OTP)
    #             updateotp = CustomUser.objects.filter(pk=user.id).update(otp=Data)
    #             ######################################################### WHATSAPP ###############################################
    #             account_sid = 'AC27512b5b2fc42f95fe7fed022ef62e6b' 
    #             auth_token = '91065766bbc30f9eabac5fc3be0954cc' 
    #             client = Client(account_sid, auth_token) 


    #             # message = client.messages.create( 
    #             #                             from_='+19803242842',  
    #             #                             body=f'Your OTP is {OTP} \nvalid for 5 minutes',      
    #             #                             to='+918799026188' 
    #             #                         ) 
    #             request.session['OTP'] = OTP
    #             otpfromlogin = request.session['OTP'] = OTP
    #             return Response("OTP sended")
    #         # else:
    #         if request.data.get('otp'):
    #             Frontend_side_otp = request.data.get('otp', None)
    #             print("--------------------------------------->> request.session: ",Frontend_side_otp)
    #             uid = request.session['ses_var']
    #             print("--------------------------------------->> uid: ", uid)
    #             Login_side= CustomUser.objects.filter(pk=uid).values('otp').first()
    #             Login_side_otp =Login_side['otp']
                
    #             if int(Frontend_side_otp) == int(Login_side_otp):
    #                 otp = request.data.get('otp', None)
    #                 user= CustomUser.objects.get(otp=otp)
    #                 token = RefreshToken.for_user(user)
    #                 if user is not None:
    #                     jwt_access_token_lifetime =  settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    #                     jwt_refresh_token_lifetime =  settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
    #                     update_last_login(None, user)
    #                     response = {
    #                         'success': 'True',
    #                         'status code': status.HTTP_200_OK,
    #                         'message': 'User logged in successfully',
    #                         'access': str(token.access_token),
    #                         'referesh_token':str(token),
    #                         "access_token_life_time_in_seconds" : jwt_access_token_lifetime.total_seconds(),
    #                         "refresh_token_life_time_in_seconds" : jwt_refresh_token_lifetime.total_seconds(),
    #                     }
    #                     status_code = status.HTTP_200_OK
    #                     return Response(response, status=status_code)
    #             else:
    #                 return Response("Didn't Match OTP")
    #             return Response("out of if you are not logged in")
    def post(self, request):
        user= request.data
        serializer= self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            if request.data.get('mobile_number') and not request.data.get('otp'):
                mobile_number = request.data.get('mobile_number', None)
                try:
                    user= CustomUser.objects.get(mobile_number=mobile_number)
                    ses_var = user.id   
                except:
                    return Response({"error": "Your username/email is not correct. Please try again or register your details"})
                ######################################################### otp ####################################################
                digits = "0123456789"
                OTP = ""
                for i in range(4):
                    OTP += digits[math.floor(random.random() * 10)]
                Data = int(OTP)
                print("--------------------------------------->> OTP:", OTP)
                updateotp = CustomUser.objects.filter(pk=user.id).update(otp=Data)
                ######################################################### WHATSAPP ###############################################
                # account_sid = 'AC27512b5b2fc42f95fe7fed022ef62e6b' 
                # auth_token = '91065766bbc30f9eabac5fc3be0954cc' 
                # client = Client(account_sid, auth_token) 
                # message = client.messages.create( 
                #                             from_='+19803242842',  
                #                             body=f'Your OTP is {OTP} \nvalid for 5 minutes',      
                #                             to='+918799026188' 
                #                         )
                # request.session['OTP'] = OTP
                # otpfromlogin = request.session['OTP'] = OTP
                return Response({"success": "OTP sended on your mobile device please check"},status.HTTP_200_OK)
            else:
                if request.data.get('mobile_number') and request.data.get('otp'):
                    mobile_number_database = request.data.get('mobile_number')
                    print("--------------------------------------->> mobile_number_database: ", mobile_number_database)
                    otp_database = request.data.get('otp')
                    print("--------------------------------------->> otp_database: ", otp_database)
                    if CustomUser.objects.all().filter(mobile_number=mobile_number_database,otp=otp_database):
                        print("------------------DATA AVAILABLE IN DB--------------------->>: ")
                        otp = request.data.get('otp', None)
                        user= CustomUser.objects.get(mobile_number=mobile_number_database,otp=otp_database)
                        token = RefreshToken.for_user(user)
                        if user is not None:
                            jwt_access_token_lifetime =  settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                            jwt_refresh_token_lifetime =  settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
                            update_last_login(None, user)
                            response = {
                                'success': 'True',
                                'status code': status.HTTP_200_OK,
                                'message': 'User logged in successfully',
                                'access': str(token.access_token),
                                'referesh_token':str(token),
                                "access_token_life_time_in_seconds" : jwt_access_token_lifetime.total_seconds(),
                                "refresh_token_life_time_in_seconds" : jwt_refresh_token_lifetime.total_seconds(),
                            }
                            status_code = status.HTTP_200_OK
                            return Response(response, status=status_code)
                    else:
                        return Response("Didn't Match otp please try again",status.HTTP_400_BAD_REQUEST)
                    return Response("out of if you are not logged in")

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)

class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes= (AllowAny, ) 
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
