from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

def auth(request):
    return render(request, "money/auth.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def menu(request):
    count = count_1 = count_2 = count_3 = count_4 = count_5 = count_6 = count_7 = 0
    posts = Post.objects.filter(author=request.user)
    for post in posts:
        count += post.summa
        if post.selector =='П':
            count_1 += post.summa
        elif post.selector == 'Т':
            count_2 += post.summa
        elif post.selector == 'О':
            count_3 += post.summa
        elif post.selector == 'С':
            count_4 += post.summa
        elif post.selector == 'А':
            count_5 += post.summa
        elif post.selector == 'Ж':
            count_6 += post.summa
        elif post.selector == 'Д':
            count_7 += post.summa
    return render(request, 'money/menu.html', {'count_1': count_1, 'count_2': count_2, 'count_3': count_3, 'count_4': count_4, 'count_5': count_5, 'count_6': count_6, 'count_7': count_7, 'count': count, })


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/menu/')

    else:
        form = PostForm()
    return render(request, 'money/for_forms.html', {'form': form})