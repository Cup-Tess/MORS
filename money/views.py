from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from json import dumps


edin = 1
SI = 'рубль'
def auth(request):
    global edin
    global SI
    if request.method == "POST":
        edin = int(request.POST.get('edin'))
        SI = request.POST.get('SI')
    edin_JS = dumps(edin)
    SI_JS=dumps(SI)
    return render(request, "money/auth.html", {"edin": edin_JS, "SI": SI_JS,})




class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

data2 = data3 = str(timezone.now())
data2 = data2[:10]+'T'+data2[11:16]
data3 = data3[:10]+'T'+data2[11:16]
dataJSON2 = dumps(data2)
dataJSON3 = dumps(data3)

def menu(request):
    global dataJSON2, dataJSON3, data2, data3, edin, SI
    edin_JS = dumps(edin)
    SI_JS = dumps(SI)
    if request.method == "POST":
        data2 = request.POST.get('data2')
        data3 = request.POST.get('data3')
        dataJSON2 = dumps(data2)
        dataJSON3 = dumps(data3)
    posts = Post.objects.filter(author=request.user).filter(published_date__range=[data2, data3])
    count = count_1 = count_2 = count_3 = count_4 = count_5 = count_6 = count_7 = 0

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
    data = [
            ['Продукты', int(count_1)],
            ['Транспорт', int(count_2)],
            ['Одежда', int(count_3)],
            ['Коммунальные услуги', int(count_4)],
            ['Аптеки', int(count_5)],
            ['Дом', int(count_6)]
        ]
    dataJSON = dumps(data)
    return render(request, 'money/menu.html', {'edin': edin_JS,'SI': SI_JS,'data': dataJSON, 'count_1': round(count_1/edin, 1), 'count_2': round(count_2/edin, 1), 'count_3': round(count_3/edin, 1), 'count_4': round(count_4/edin, 1), 'count_5': round(count_5/edin, 1), 'count_6': round(count_6/edin, 1), 'count_7': round(count_7/edin, 1), 'count': round(count/edin, 1),'dataJSON2':dataJSON2, 'dataJSON3': dataJSON3,})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        data1 = request.POST.get('data1')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = data1
            post.save()
            return redirect('/menu/')

    else:
        form = PostForm()
    return render(request, 'money/for_forms.html', {'form': form})

def history(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'money/history.html', {'posts': posts})
