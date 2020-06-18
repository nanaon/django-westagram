# from django.shortcuts import render
import json
from django.views import View
from django.http import JsonResponse, HttpResponse
# from django.core.validators import validate_email
from .models import Users
import bcrypt
import jwt

class MainView(View):
    def get(self, request):
        return JsonResponse({'Welcome to':'Westagram', 'Sign-up':'/users/sign-up', 'Log-in':'/users/log-in'}, status=200)

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            # validate_email(data['email'])
             
            hased_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hased_pw.decode('utf-8')

            if data['username'] == '':
                return JsonResponse({'message':'username is required.'}, status=401)
            
            elif data['password'] == '':
                return JsonResponse({'message':'password is required.'}, status=401)
            
            elif Users.objects.filter(username=data['username']).exists():
                return JsonResponse({'message':'username already exists.'}, status=409)
            
            if not Users.objects.filter(username=data['username']).exists():
                Users(
                    username = data['username'],
                    password = decoded_hashed_pw
                ).save()
                return JsonResponse({'message':'WELCOME, ' + data['username']}, status=200)

        except IntegrityError:
            return JsonResponse({'message':'username already exists.'}, status=409)
       
       # except ValidationError:

        except KeyError as e:
            return JsonResponse({'message': str(e) + ' is right key name. The key names are username and password.'}, status=400)

        except:
             return JsonResponse({'message':'Something wrong.'}, status=401)
        

    def get(self, request):
        return JsonResponse({'Please':'Sign-up'}, status=200)

class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Users.objects.filter(username=data['username']).exists():
                
                user_id = Users.objects.get(username=data['username'])
                
                if bcrypt.checkpw(data['password'].encode('utf-8'), user_id.password.encode('utf-8')) == True:
                    access_token = jwt.encode({'id':user_id.id}, 'secret', algorithm='HS256')
                    return JsonResponse({'message':'WELCOME BACK, ' + data['username'], 'token' : access_token.decode('utf-8')}, status=200)
                else:
                    return JsonResponse({'message':'Wrong password.'}, status=401)
            else:
                return JsonResponse({'message':'Wrong username.'}, status=401)
        
        #except Users.DoesNotExist:
        except KeyError as e:
            return JsonResponse({'message': str(e) + ' is right key name. The key names are username and password.'}, status=400)


    


    def get(self, request): # get으로 body에 정보를 보내는 법 찾아보기 / # int, str, slug
        login_data = Users.objects.filter(username=data['username']).values()
        return JsonResponse({'user':list(login_data)}, status=200)
