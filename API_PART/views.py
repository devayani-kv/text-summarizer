from django.shortcuts import render
from . forms import dataForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from . models import data
from .serializers import dataSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib import messages
from . import extract 

# Create your views here.

class dataView(viewsets.ModelViewSet):
    queryset = data.objects.all()
    serializer_class = dataSerializer

#@api_view(["POST"])
def final_ans(request):
    try:
        dta = request.data
        print(dta)
        return JsonResponse('your ans is suxess', safe = False)
    except ValueError as e:
        print('error = ', e)
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
    
def weird_name(request):
    #print('rhbakj')
    print(request)
    #print('req method = ', request.method)
    #form = dataForm(request.GET)
    if request.method == 'POST':
        print('HEREEEEEE')
        form = dataForm(request.POST)
        if form.is_valid():
            print('inside')
            link = form.cleaned_data['link']
            text = form.cleaned_data['inputtext']
            option = form.cleaned_data['option']
            print(link, text, option)
            ans = ''
            if link != '':
                if option == 'Extractive':
                    txt = extract.get_data_from_url(link)
                    ans = extract.generate_summary_extractive(txt, 10)
                elif option == 'Abstractive':
                    ans = extract.generate_summary_abstractive(text)
            else:
                if option == 'Extractive':
                    ans = extract.generate_summary_extractive(text, 10)
                elif option == 'Abstractive':
                    ans = extract.generate_summary_abstractive(text)
            messages.success(request, 'Summarized Text: {}'.format(ans))
            
    form = dataForm()

    return render(request, 'myform/weird_name.html', {'form':form})
    #return render(request, 'myform/ww.html')