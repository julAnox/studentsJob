from django.contrib import admin
from django.urls import path

from echoApp.views import home, login, signup, profile, vacancies, logout, get_countries, \
    filter_vacancies, vacancy, my_summaries, create_summary, my_company, change_vacancy_publish, \
    delete_vacancy, add_company, summaries, summary

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('logout', logout, name='logout'),
    path('profile', profile, name='profile'),
    path('summaries', summaries, name='summaries'),
    path('summary/<int:pk>', summary, name='summary'),
    # path('my_summaries', my_summaries, name='my_summaries'),
    # path('createsummary', create_summary, name='create_summary'),
    path('my_company', my_company, name='my_company'),
    path('add_company', add_company, name='add_company'),
    path('api/change_vacancy_publish/<int:pk>', change_vacancy_publish, name='change_vacancy_publish'),
    path('api/delete_vacancy/<int:pk>', delete_vacancy, name='delete_vacancy'),
    path('vacancy/<int:pk>', vacancy, name='vacancy'),
    path('vacancies', vacancies, name='vacancies'),

    path('api/countries', get_countries, name='get_countries'),
    # path('api/filter_vacancies', filter_vacancies, name='filter_vacancies'),
]
