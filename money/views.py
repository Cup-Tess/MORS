from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Datas
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from json import dumps
import xlwt
from django.http import HttpResponse
import numpy as np
from sklearn.linear_model import LinearRegression


def auth(request):
    edin = 1
    SI = 'рубль'
    if request.method == "POST":
        edin = int(request.POST.get('edin'))
        SI = request.POST.get('SI')
        posts = Datas.objects.filter(author=request.user)
        length = len(posts)
        if length == 0:
            p = Datas()
            p.author = request.user
            data2 = data3 = str(timezone.now())
            p.data1 = data2[:10] + 'T' + data2[11:16]
            p.data2 = data3[:10] + 'T' + data2[11:16]
            p.save()
        else:
            p = Datas.objects.get(author=request.user)
            p.edin = edin
            p.SI = SI
            p.save()
        if "but0" in request.POST:
            return redirect('/menu')

    edin_JS = dumps(edin)
    SI_JS = dumps(SI)
    return render(request, "money/auth.html", {"edin": edin_JS, "SI": SI_JS, })


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def menu(request):
    p = Datas.objects.get(author=request.user)
    data2 = str(p.data1)
    data3 = str(p.data2)
    data2 = data2[:10] + 'T' + data2[11:16]
    data3 = data3[:10] + 'T' + data2[11:16]
    dataJSON2 = dumps(data2)
    dataJSON3 = dumps(data3)
    edin = p.edin
    SI = p.SI
    edin_JS = dumps(edin)
    SI_JS = dumps(SI)
    if request.method == "POST":
        data2 = request.POST.get('data2')
        data3 = request.POST.get('data3')
        p.data1 = data2[:10] + " " + data2[11:]
        p.data2 = data3[:10] + " " + data3[11:]
        dataJSON2 = dumps(data2)
        dataJSON3 = dumps(data3)
    posts = Post.objects.filter(author=request.user).filter(published_date__range=[p.data1, p.data2])
    count = count_1 = count_2 = count_3 = count_4 = count_5 = count_6 = count_7 = 0

    for post in posts:
        if post.selector != 'Д':
            count += post.summa
            if post.selector == 'П':
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
        else:
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
    ost = count_7 - count
    p.ost = round(ost / edin, 1)
    p.save()
    return render(request, 'money/menu.html', {'edin': edin_JS, 'SI': SI_JS, 'data': dataJSON,
                                               'count_1': round(count_1 / edin, 1), 'count_2': round(count_2 / edin, 1),
                                               'count_3': round(count_3 / edin, 1), 'count_4': round(count_4 / edin, 1),
                                               'count_5': round(count_5 / edin, 1), 'count_6': round(count_6 / edin, 1),
                                               'count_7': round(count_7 / edin, 1), 'count': round(count / edin, 1),
                                               'dataJSON2': dataJSON2, 'dataJSON3': dataJSON3, })


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        data_get = request.POST.get('data1')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = data_get[:10] + " " + data_get[11:]
            post.save()
            return redirect('/menu/')

    else:
        form = PostForm()
    return render(request, 'money/for_forms.html', {'form': form})


def history(request):
    def prognoz(request):
        posts = Post.objects.filter(author=request.user).order_by('published_date')
        tz = str(timezone.now())
        tz = tz[:7]
        x_1 = []
        y_1 = []
        dat = 0
        count = posts[0].summa
        for i in range(1, len(posts)):
            k = posts[i].published_date
            d = posts[i - 1].published_date
            if posts[i].selector != "Д":
                if k[:7] == d[:7]:
                    count += posts[i].summa
                else:
                    y_1.append(float(count))
                    x_1.append(float(y_1.index(float(count))))
                    if tz == d[:7]:
                        dat = 1
                        month = y_1.index(float(count))
                    count = posts[i].summa
        y_1.append(float(count))
        x_1.append(float(y_1.index(float(count))))
        if tz == d[:7]:
            dat = 1
            month = y_1.index(float(count))
        x = np.array(x_1).reshape((-1, 1))
        y = np.array(y_1)
        model = LinearRegression()
        model.fit(x, y)
        model = LinearRegression().fit(x, y)
        if dat == 1:
            x_new = np.array([month]).reshape((-1, 1))
        else:
            x_new = np.array([month+1]).reshape((-1, 1))
        y_pred = model.predict(x_new)
        return y_pred

    prog = prognoz(request)
    p = Datas.objects.get(author=request.user)
    post = Post.objects.filter(author=request.user).filter(published_date__range=[p.data1, p.data2])
    return render(request, 'money/history.html',
                  {'prognoz':round(prog[0], 1), 'posts': post, "data1": p.data1, "data2": p.data2, "ost": p.ost})


def export_post_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="post.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Post')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Сумма', 'Категория', 'Заметки', 'Дата публикации', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Post.objects.filter(author=request.user).values_list('summa', 'selector', 'notes', 'published_date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

