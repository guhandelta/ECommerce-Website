from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect   


from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
    context = {
        "title" : "Welcome",
        "content" : "This is the Home Page",
    }
    if request.user.is_authenticated():
        context["premium_content"] = "YEAH!!!!!"
    return render(request, "home_page.html", context)

def contact_page(request):
    contactForm = ContactForm(request.POST or None)
    context = {
        "title" : "Welcome",
        "content" : "This is the Contact Page",
        "form" : contactForm 
        
    }
    if contactForm.is_valid():
        print(contactForm.cleaned_data)
    # if request.method == "POST":
    #     #print(request.POST)
    #     print(request.POST.get("fullname"))
    #     print(request.POST.get("email")) 
    #     print(request.POST.get("content"))
    return render(request, "contact/view.html", context)

def about_page(request):
    context = {
        "title" : "Welcome",
        "content" : "This is the About Page"
    }
    return render(request, "home_page.html", context)

def login_page(request):
    form=LoginForm(request.POST or None)
    context = {
        "form" : form
    }
    print("User Logged in:")
    #print(request.user.is_authenticated())
    if form.is_valid():
        print(form.cleaned_data)
        uname = form.cleaned_data.get("username")
        pwd = form.cleaned_data.get("password")
        user = authenticate(request, username=uname, password=pwd)
        print(user)
        #print(request.user.is_authenticated())  
        if user is not None:
            #print(request.user.is_authenticated())
            login(request,user)
            context['form'] = LoginForm()
            return redirect("/login")
        else:
            print("Error")
    return render(request, "auth/login.html", context)

user=get_user_model() 
def register_page(request):
    form=RegisterForm(request.POST or None)
    context = {
        "form" : form
    }
    if form.is_valid():
        print(form.cleaned_data)
        uname = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        pwd = form.cleaned_data.get("password")
        new_user=user.objects.create_user(uname, email, pwd)
        print(new_user)
    return render(request, "auth/register.html", context)

def home_page_old(request):
    return HttpResponse("Hello World")
    