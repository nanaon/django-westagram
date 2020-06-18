# from django.shortcuts import render

import json
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import Comments

from users.utils import auth 

class CommentView(View):
    @auth
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            if data['comment'] == '':
                return HttpResponse(status=400)

            Comments(
                username_id = user.id,
                comment = data['comment'],
            ).save()

            return JsonResponse({'comment': data['comment']}, status=200)
       
        except KeyError as e:
            return JsonResponse({'message': e + 'Invalid key. The key name is comment.'})
        
        #except (
            #CryptoException,
            #jwt.exceptions.DecodeError,
            #jwt.ExpiredSignature,
            #User.DoesNotExist,
        #):
            #raise BadRequest('Invalid token.')


        except jwt.exceptions.InvalidSignatureError:
            raise Exception('Invalide token.')
            #return JsonResponse({'message':'Invalid token.'}, status=401)

        except jwt.exceptions.DecodeError:
            raise Exception('Invalid token.')
            #return JsonResponse({'message':'Invalid token.'}, status=401)

        #except Exception as a:
            #return a

        except:
            return JsonResponse({'message':'Something wrong.'}, status=401)


    def get(self, request):
        comment_list = Comments.objects.values()
        return JsonResponse({'comments':list(comment_list)}, status=200)
