from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from gifs.models import *
from gifs.serializers import *

@api_view(['GET'])
def gifs_list(request):
    if request.method == 'GET':
        gif = Gif.objects.all()[:10]
        serializer = GifSerializer(gif, many=True)
        return JsonResponse(serializer.data, safe=False)

