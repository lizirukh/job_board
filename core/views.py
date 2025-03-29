from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import VacancyForm, ApplicationForm
from .mixins import AddVacancyMixin
from .models import Vacancy, Application
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'events/vacancy_list.html'
    context_object_name = 'vacancies'
    paginate_by = 1

    def get_queryset(self):
        title = self.request.GET.get('title')
        company = self.request.GET.get('company')

        filters = Q()

        if title and company:
            filters &= Q(title__icontains=title) & Q(company__name__icontains=company)
        elif title:
            filters |= Q(title__icontains=title)
        elif company:
            filters |= Q(company__icontains=company)

        if title or company:
            vacancies = self.model.objects.filter(filters)
        else:
            vacancies = self.model.objects.all()

        return vacancies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class VacancyDetailView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'events/vacancy_detail.html'

    # def vacancy_detail_page(request, pk):
    #     vacancy = get_object_or_404(Vacancy, pk=pk)


class VacancyCreateView(LoginRequiredMixin, AddVacancyMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'events/add_vacancy.html'
    success_url = reverse_lazy('vacancy_list')

    def form_valid(self, form):
        vacancy = form.save()

        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'events/application_form.html'

    def get_success_url(self):
        return reverse_lazy('vacancy_detail', kwargs={'pk': self.kwargs['vacancy_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(Vacancy, pk=self.kwargs['vacancy_id'])
        return context

    def form_valid(self, form):
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs['vacancy_id'])
        application = form.save(commit=False)
        application.vacancy = vacancy
        application.save()

        subject = f'New Application for {vacancy.title}'
        message = f'''
        New application received:

        Position: {vacancy.title}
        Applicant: {application.first_name} {application.last_name}
        Location: {vacancy.location}
        Email: {application.email}
        Date: {application.applying_date}

        Motivational Letter:
        {application.motivational_letter}

        Please see the attached CV.
        '''

        recipient_email = vacancy.company_email

        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
        )

        if application.cv:
            try:
                email.attach(
                    application.cv.name,
                    application.cv.read(),
                    'application/octet-stream'
                )
            except FileNotFoundError:
                pass

        email.send()

        return super().form_valid(form)


class CompanyVacancyListView(ListView):
    model = Vacancy
    template_name = 'events/company_vacancies.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        company = self.request.user.company
        return Vacancy.objects.filter(company=company)


# class VacancyDeleteView(LoginRequiredMixin, DeleteView):
#     model = Vacancy
#     # template_name = 'events/book_confirm_delete.html'
#     success_url = reverse_lazy('vacancy_list')