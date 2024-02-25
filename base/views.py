from django.http import  HttpResponse
from base.models import Post
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm
from django.db.models import Q
import mimetypes

# Create your views here.

def loginView(request):

    if request.user.is_authenticated:
        return redirect('base/home.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
                user = User.objects.get(username = username)
        except:
                messages.error(request, 'User does not exist')

                user = authenticate(request, username = username, password = password)

        else:
            messages.error(request, 'Username or Password does not exist')

            if user is not None:
                login(request, user)
                return redirect('home')
        
            else:
                messages.error(request, 'User does not exist')


    context = {}
    return render(request, 'base/login_register.html',context)

def LogoutView(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'An error occured during signup')

    return render(request, 'base/user_registration.html' ,{'form':form})

def home(request): 
    context = {
        'posts': Post.objects.all(),

        }
    return render(request, 'base/home.html', context)

def search(request):
    template='base/search.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    context={ 'posts':result }
    return render(request,template,context)
   
def download_file(request):
    fl_path = '/file/path'
    filename = 'download_file_name.extension'

    fl = open(fl_path, 'r')
    mime_type, _= mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] ="attachment; filename= %s "% filename
    return render(request, response)

class PostListView(ListView):
    model = Post
    template_name = 'base/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class UserPostListView(ListView):
    model = Post
    template_name = 'base/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'base/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
        model = Post
        template_name = 'base/post_detail.html'

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView):
    model = Post
    template_name = 'base/post_form.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin ,DeleteView):
    model = Post
    success_url = '/'
    template_name = 'base/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

