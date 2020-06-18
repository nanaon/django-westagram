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
        
        hased_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        decoded_hashed_pw = hased_pw.decode('utf-8')

        try:
            # validate_email(data['email'])
            if data['username'] == '':
                return JsonResponse({'message':'ID_IS_REQUIRED'}, status=401)
            
            elif data['password'] == '':
                return JsonResponse({'message':'PASSWORD_IS_REQUIRED'}, status=401)
            
            elif Users.objects.filter(username=data['username']).exists():
                return JsonResponse({'message':'ID_EXISTS'}, status=409)
            
            elif not Users.objects.filter(username=data['username']).exists():
                Users(
                    username = data['username'],
                    password = decoded_hashed_pw
                ).save()
                return JsonResponse({'message':'WELCOME'}, status=200)

        # except IntegrityError: - 아이디 중복검사. models에서 unique = True 설정해준다.
        # except ValidationError:


        except:
             return JsonResponse({'message':'INVALID_ID'}, status=401)
        

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
                    print(1)
                    return JsonResponse({'token': access_token.decode('utf-8')}, status=200)
                else:
                    return JsonResponse({'message':'비밀번호가 틀립니다.'}, status=401)
            else:
                print(2)
                return JsonResponse({'message':'아이디가 없습니다.'}, status=401)
        
        #except Users.DoesNotExist:
        #except KeyError:

        except Exception as e:
            print(3)
            return e
            #return JsonResponse({'message':'INVALID_USER'}, status=401)
    


    def get(self, request): # get으로 body에 정보를 보내는 법 찾아보기 / # int, str, slug
        login_data = Users.objects.filter(username=data['username']).values()
        return JsonResponse({'user':list(login_data)}, status=200)
