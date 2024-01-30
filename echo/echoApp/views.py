from django.conf import settings
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from echoApp.models import *
from echoApp.validators import email_validator
from echoApp.backend import get_user, fast_hash, is_user_auth, is_has_company


@api_view(["GET"])
def get_countries(request):
    countries = Country.objects.all()
    clean_data = []
    for country in countries:
        country_data = {country.title: []}
        regions = Region.objects.filter(country=country)
        for region in regions:
            region_data = {region.title: []}
            districts = District.objects.filter(region=region)
            for district in districts:
                region_data[region.title].append(district.title)
            country_data[country.title].append(region_data)
        clean_data.append(country_data)
    return JsonResponse({"clean_data": clean_data})


def home(request):
    comments = Comment.objects.all()
    if request.method == 'POST':
        if not 'user' in request.POST :
            if request.POST['text'] != '':
                session = request.session
                user = session.get(settings.USER_SESSION_ID)
                user_obj = User.objects.get(id=user['user'])
                Comment.objects.create(user=f'{user_obj.first_name} {user_obj.last_name}', text=request.POST['text'], photo=user_obj.img)
        elif request.POST['user'] != '' and request.POST['text'] != '':
            Comment.objects.create(user=request.POST['user'], text=request.POST['text'])
    context = {
        'comments': comments
    }
    if is_user_auth(request) != None:
        context['auth_user'] = User.objects.get(id=is_user_auth(request))
    return render(request, 'echoApp/home.html', context=context)


def vacancies(request):
    context = {}
    if is_user_auth(request) != None:
        context['auth_user'] = User.objects.get(id=is_user_auth(request))
    vacancies = Vacancy.objects.filter(is_publish=True)
    context['vacancies'] = vacancies
    return render(request, 'echoApp/vacancies.html', context=context)


def filter_vacancies(request):
    qwe = request.GET
    return HttpResponse({'status': 'ok'})


def vacancy(request, pk):
    context = {}
    if request.method == 'GET':
        if is_user_auth(request) != None:
            context['auth_user'] = User.objects.get(id=is_user_auth(request))
        context['vacancy'] = Vacancy.objects.get(id=pk)
        return render(request, 'echoApp/vacancy.html', context=context)
    elif request.method == 'POST':
        vacancy = Vacancy.objects.get(id=pk)
        vacancy.responses = F('responses') + 1
        vacancy.save()
        Response.objects.create(message=request.POST['message'], vacancy_id=pk, user=User.objects.get(id=is_user_auth(request)))
        return redirect('vacancies')


def summaries(request):
    context = {}
    if is_user_auth(request) != None:
        context['auth_user'] = User.objects.get(id=is_user_auth(request))
    context['summaries'] = Summary.objects.filter(is_publish=True)
    return render(request, 'echoApp/summaries.html', context=context)


def summary(request, pk):
    context = {}
    if is_user_auth(request) != None:
        context['auth_user'] = User.objects.get(id=is_user_auth(request))
    context['summary'] = Summary.objects.get(id=pk)
    return render(request, 'echoApp/summary.html', context=context)


def login(request):
    if not is_user_auth(request):
        context = {}
        if request.method == "POST":
            context['error'] = 'Email is invalid'
            if email_validator(request.POST['email']) == True:
                context['error'] = 'This email does not exist'
                if get_user(request.POST['email']):
                    context['error'] = 'Incorrect password'
                    user_obj = User.objects.filter(email=request.POST['email'], password=fast_hash(request.POST['password']))
                    if len(user_obj) == 1:
                        session = request.session
                        user = session[settings.USER_SESSION_ID] = {}
                        user['user'] = user_obj[0].id
                        return redirect('home')
        return render(request, 'echoApp/login.html', context=context)
    return redirect('home')


def signup(request):
    if not is_user_auth(request):
        context = {}
        if request.method == "POST":
            context['error'] = 'Email is invalid'
            if email_validator(request.POST['email']) == True:
                context['error'] = 'This email already in use'
                if not get_user(request.POST['email']):
                    context['error'] = 'Incorrect password'
                    if request.POST['password1'] == request.POST['password2']:
                        user_obj = User.objects.create(email=request.POST['email'], password=fast_hash(request.POST['password1']))
                        session = request.session
                        user = session[settings.USER_SESSION_ID] = {}
                        user['user'] = int(user_obj.id)
                        return redirect('home')
        return render(request, 'echoApp/signup.html', context=context)
    return redirect('home')


def profile(request):
    if is_user_auth(request):
        context = {}
        if request.method == "GET":
            context['auth_user'] = User.objects.get(id=is_user_auth(request))
            try:
                context['company'] = Company.objects.get(creator=is_user_auth(request))
            except:
                context['company'] = None
            return render(request, 'echoApp/profile.html', context=context)
        elif request.method == "POST":
            user_obj = User.objects.get(email=request.POST['email'])
            try:
                user_obj.img = request.FILES['img']
            except:
                user_obj.img = user_obj.img
            user_obj.first_name = request.POST['first_name']
            user_obj.last_name = request.POST['last_name']
            user_obj.birthday = request.POST['birthday']
            user_obj.gender = request.POST.get('gender')
            user_obj.phone = request.POST['phone']
            try:
                user_obj.country = Country.object.get(title=request.POST.get('country'))
                user_obj.region = Region.object.get(title=request.POST.get('region'))
                user_obj.district = District.object.get(title=request.POST.get('district'))
            except:
                pass
            user_obj.save()
            context['auth_user'] = user_obj
            return render(request, 'echoApp/profile.html', context=context)
    return redirect('home')


def my_summaries(request):
    context = {}
    if is_user_auth(request) != None:
        context['auth_user'] = User.objects.get(id=is_user_auth(request))
    return render(request, 'echoApp/my_summaries.html', context=context)


def create_summary(request):
    context = {}
    if is_user_auth(request) != None:
        context['auth_user'] = User.objects.get(id=is_user_auth(request))
    return render(request, 'echoApp/my_summaries.html', context=context)


def add_company(request):
    context = {}
    user = is_user_auth(request)
    if user != None:
        if is_has_company(user):
            print(is_has_company(user))
            return redirect('my_company')
        else:
            context['auth_user'] = User.objects.get(id=is_user_auth(request))
            context['country'] = Country.objects.all()
            if request.method == 'POST':
                company = Company(title=request.POST['title'],
                                  country=Country.objects.get(title=request.POST.get('country')),
                                  description=request.POST['description'],
                                  creator_id=user,
                                  logo=request.FILES['logo'])
                company.save()
                return redirect('my_company')
    return render(request, 'echoApp/add_company.html', context=context)


def my_company(request):
    context = {}
    if is_user_auth(request) != None:
        user = User.objects.get(id=is_user_auth(request))
        context['auth_user'] = user
        if is_has_company(user):
            company = is_has_company(user)
            context['company'] = company
            vacancies = Vacancy.objects.filter(company=company)
            context['vacancies'] = vacancies
            context['country'] = Country.objects.all()
            if request.method == "POST":
                if request.POST.get('logo') != None:
                    user_company = Company.objects.get(id=company.id)
                    try:
                        user_company.logo = request.FILES['logo']
                    except:
                        user_company.logo = user_company.logo
                    user_company.title = request.POST['title']
                    user_company.country = Country.objects.get(title=request.POST['country'])
                    user_company.description = request.POST['description']
                    user_company.save()
                    context['company'] = user_company
                else:
                    vacancy_data = {
                        'title': request.POST['title'],
                        'description': request.POST['description'],
                        'salary': request.POST['salary'],

                        'country': Country.objects.get(title=request.POST['country']),
                        'region': Region.objects.get(title=request.POST['region']),
                        'district': District.objects.get(title=request.POST['district']),

                        'company': company,

                        'experience': request.POST.get('experience'),
                        'currency': request.POST.get('currency'),
                        'education': request.POST.get('education'),
                        'employment': request.POST.get('employment'),
                    }
                    Vacancy.objects.create(**vacancy_data)

        else:
            return redirect('add_company')
    return render(request, 'echoApp/my_company.html', context=context)


def change_vacancy_publish(request, pk):
    user = is_user_auth(request)
    if user:
        vacancy = Vacancy.objects.get(id=pk)
        if user == vacancy.company.creator.id:
            if vacancy.is_publish == True:
                vacancy.is_publish = False
                vacancy.save()
            else:
                vacancy.is_publish = True
                vacancy.save()
            return redirect('my_company')
    return redirect('home')


def delete_vacancy(request, pk):
    user = is_user_auth(request)
    if user:
        vacancy = Vacancy.objects.get(id=pk)
        if user == vacancy.company.creator.id:
            vacancy.delete()
            return redirect('my_company')
    return redirect('home')


def create_business(request):
    context = {}
    if is_user_auth(request) != None:
        context['auth_user'] = User.objects.get(id=is_user_auth(request))
    return render(request, 'echoApp/create_business', context=context)


def logout(request):
    del request.session['user']
    return redirect('home')
