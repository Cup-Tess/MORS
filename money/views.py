from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

def auth(request):
    return render(request,"money/auth.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def menu(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'money/menu.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
    else:
        form = PostForm()
    return render(request, 'money/for_forms.html', {'form': form})