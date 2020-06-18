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
            Comments(
                username_id = user.id,
                comment = data['comment'],
            ).save()

            return JsonResponse({'message': data['comment'] + ' has added.'}, status=200)
        
        except:
            return JsonResponse({'message':''}, status=401)


    def get(self, request):
        comment_list = Comments.objects.values()
        return JsonResponse({'comments':list(comment_list)}, status=200)
