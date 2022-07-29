from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
from django.http import HttpResponse
from django.contrib.auth.models import User
from blogapp.forms import UserRegistrationForm,LoginForm,UserProfileForm,PasswordResetForm,ProfilePicForm,BlogForm,CommentsForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from blogapp.models import UserProfile,Blogs,Comments
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.mail import send_mail



# Create your views here.


class SignUpView(CreateView):
    template_name="signup.html"
    form_class=UserRegistrationForm
    model=User
    success_url = reverse_lazy("signin")                     #for redirecting after successfull signup
    def form_valid(self, form):
        email=form.cleaned_data.get("email")
        form.save()
        send_mail(
            "account creation",
            "account has bee activated",
            "bharathkrishnans480@gmail.com",
            ["email"],
            fail_silently=True
        )
    # def get(self,request,*args,**kwargs):
    #     form=self.form_class()
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("signup")
    #     else:
    #         return render(request, self.template_name, {"form": form})

class SignInView(FormView):                   #get method already exists in FormView,so write only code for POST
    template_name='signin.html'
    form_class=LoginForm
    model=User
    def post(self,request,*args,**kwargs):
        form=self.form_class()
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(username=uname,password=pwd)
        if user:
            login(request, user)
            messages.success(request,"login success")
            return redirect('feed')

        else:
            messages.error(request,"invalid ID or Password")
            return render(request,'signin.html',{'form':form})
def log_outView(request,*args,**kwargs):
    if request.user:
        authenticate(logout)
        return redirect("signin")

class IndexView(CreateView):
    model=Blogs
    form_class = BlogForm
    template_name='home.html'
    success_url = "home"

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,"submission successfull")
        self.object=form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["blogs"]=Blogs.objects.all().order_by("-posted_date")              #assigning a key "blogs" and calling all objects from database and order_by for sorting,- for ascending order
        comment_form=CommentsForm()                                                #.exclude instead of .all() to exclude and ,ention the user
        context["comment_form"]=comment_form
        return context



class CreateProfileView(CreateView):
    model=UserProfile
    template_name='add-profile.html'
    form_class=UserProfileForm
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,'profile added successfully')
        self.object=form.save()
        return super().form_valid(form)

class ProfileView(TemplateView):
    template_name = 'view-profile.html'

class PasswordResetView(FormView):
    template_name = 'passwordreset.html'
    form_class = PasswordResetForm
    def post(self, request, *args, **kwargs):
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("old_password")
            password1=form.cleaned_data.get("new_password")
            password2=form.cleaned_data.get("confirm_password")
            user=authenticate(request,username=request.user.username,password=oldpassword)
            if user:
                user.set_password(password2)
                user.save()
                messages.success(request,"password successfully updated")
                return redirect("signin")
            else:
                messages.error(request,"invalid credentials")
                return redirect(request,self.template_name,{"form":form})
class ProfileUpdateView(UpdateView):
    template_name = 'editprofile.html'
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy("feed")
    pk_url_kwarg = "user_id"                       #overriding the pk_url_kwarg=pk value to user_id

    def form_valid(self, form):                    #overriding form_valid method to add messages,applicable only in places with post method
        form.instance.user = self.request.user
        messages.success(self.request, 'profile updated successfully')
        self.object = form.save()
        return super().form_valid(form)


class ProPicView(UpdateView):
    template_name = 'propic.html'
    model = UserProfile
    form_class = ProfilePicForm
    success_url = reverse_lazy("pro-pic")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"updated successfully")
        self.object=form.save()
        return super().form_valid(form)

def add_comment(request,*args,**kwargs):
    if request.method=="POST":
        blog_id=kwargs.get("post_id")
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get("comment")
        Comments.objects.create(blog=blog,comment=comment,user=user)
        messages.success(request,"comment successfully posted")
        return redirect("feed")

def add_like(request,*args,**kwargs):
    blog_id=kwargs.get("post_id")
    blog=Blogs.objects.get(id=blog_id)
    if blog.liked_by.filter(id=request.user.id).exists():
        blog.liked_by.remove(request.user)
    else:
        blog.liked_by.add(request.user)
    return redirect("feed")
def follow_friend(request,*args,**kwargs):
    friend_id=kwargs.get("user_id")
    friend_profile=User.objects.get(id=friend_id)
    request.user.users.following.add(friend_profile)
    messages.success(request,"you are started following")
    return redirect("feed")

class NewIndexView(CreateView):
    model=Blogs
    form_class = BlogForm
    template_name='feed.html'
    success_url = "feed"

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,"submission successfull")
        self.object=form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["blogs"]=Blogs.objects.all().order_by("-posted_date")              #assigning a key "blogs" and calling all objects from database and order_by for sorting,- for ascending order
        comment_form=CommentsForm()                                                #.exclude instead of .all() to exclude and ,ention the user
        context["comment_form"]=comment_form
        return context
class DesignView(CreateView):
    model=Blogs
    form_class = BlogForm
    template_name='design.html'
    success_url = "design"

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,"submission successfull")
        self.object=form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["blogs"]=Blogs.objects.all().order_by("-posted_date")              #assigning a key "blogs" and calling all objects from database and order_by for sorting,- for ascending order
        comment_form=CommentsForm()                                                #.exclude instead of .all() to exclude and ,ention the user
        context["comment_form"]=comment_form
        return context


class Base1_View(TemplateView):
    template_name = 'base1.html'
class Following_Page_View(TemplateView):
    template_name = 'following.html'
class AboutUs_View(TemplateView):
    template_name = "aboutus.html"





