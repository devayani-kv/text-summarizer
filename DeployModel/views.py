from django.http import HttpResponse
from django.shortcuts import render
#from . import extract

def home(request):
    return HttpResponse(request)

#def result(request):
    #lis = []
    #lis.append(request.GET)
    #print('LINK ',request.GET['link'])
    #link = request.GET['link']
    #print('TEXT ', request.GET['inputtext_'])
    #text = request.GET['inputtext_']
    #print('OPTION ', request.GET['option'])
    #option = request.GET['option']
    #ans = extract.get_ip()
    #return render(request, "result.html")