from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    list =[
        {'id':12,'name':'anubhav', 'age':54},
        {'id':43,'name':'bharav', 'age':41},
        {'id':5,'name':'vaibhav', 'age':16},
        {'id':7,'name':'raghav', 'age':36},
        {'id':23,'name':'danav', 'age':24}
    ]
    return render(request,'worker.html', context={'list':list})