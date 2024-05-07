from django.shortcuts import render,redirect
from .models import*
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/login/")
def receipe(request):

    if request.method=="POST":
        #taking data input from reciepe.html by using request and .get method
        data=request.POST 
        receipe_image=request.FILES.get('receipe_image')
        receipe_name= data.get('receipe_name')
        receipe_description= data.get('receipe_description')
        
       # print(receipe_name)
       # print(receipe_description)
       # print(receipe_image)
    
        #print(data)
    # calling the Reciepe function "object.create" in the models.py to put the data in the db
        #logic for adding data 
        Receipe.objects.create(
        receipe_name=receipe_name, 
        receipe_description=receipe_description, 
        receipe_image=receipe_image, )

        return redirect('/receipe/')
    
    #calling the function "object.all" to get all the data in db
    queryset= Receipe.objects.all()

    if request.GET.get('search'):
        print(request.GET.get('search'))
        queryset=queryset.filter(receipe_name__icontains = request.GET.get('search'))

    else:
        queryset= Receipe.objects.all()

    context={"receipes": queryset}
    return render(request,'receipe.html',context)




#update functionality rendering update html page
def update_receipe(request, id):

    #database se object ko call kr k uska refrence querset mai pass kia
    queryset = Receipe.objects.get(id=id)

#taking input and cheking logic    
    if request.method=="POST":
        #fetching the data from update html input
        data=request.POST 
        receipe_image=request.FILES.get('receipe_image')
        receipe_name= data.get('receipe_name')
        receipe_description= data.get('receipe_description')  

        #refrence object k lia value set kia
        queryset.receipe_name=receipe_name 
        queryset.receipe_description=receipe_description 

        #logic to check if any new image from update html
        if receipe_image:
            queryset.receipe_image=receipe_image

        #updated value ko save kr lia db mai
        queryset.save()
        return redirect('/receipe/') 

    context={"receipes": queryset}
    return render(request,'update_receipe.html',context)




def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    #print(queryset)
    queryset.delete()
    return redirect('/receipe/')


def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username =username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/receipe/')
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')


def register_page(request):
    
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')


        user = User.objects.filter(username =username)

        if user.exists():
            messages.info(request, "Username already exists")
            #messages.warning(request, "Username already exists")
            return redirect('/register/')

        user =User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username= username
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account Created Sucessfuly")
        return redirect('/register/')
    
    return render(request,'register.html')