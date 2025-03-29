from django.urls import path
from . import views
from .views import ApplicationCreateView, CompanyVacancyListView

urlpatterns = [
    path('', views.VacancyListView.as_view(), name='vacancy_list'),
    path('vacancy/<int:pk>', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('vacancy/add/', views.VacancyCreateView.as_view(), name='vacancy_add'),
    # path('vacancy/delete/<int:pk>', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    # path('application/add/', views.ApplicationCreateView.as_view(), name='application_add'),
    path('<int:vacancy_id>/apply/', ApplicationCreateView.as_view(), name='apply_vacancy'),
    path('company/', CompanyVacancyListView.as_view(), name='company_vacancies'),
]

