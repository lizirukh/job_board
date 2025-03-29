from django.db import models

LOCATION_CHOICES = (
    ('Tbilisi', 'Tbilisi'),
    ('Telavi', 'Telavi'),
    ('Batumi', 'Batumi'),
    ('Kutaisi', 'Kutaisi'),
    ('Rustavi', 'Rustavi'),
)

class Category(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'

class Company(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'

class Vacancy(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies', null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vacancies', null=False, blank=False)
    was_published = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, null=False, blank=False)
    company_email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'vacancies'

class Application(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)  # Added for SMTP
    motivational_letter = models.TextField(null=True, blank=True)
    applying_date = models.DateField(auto_now_add=True)
    cv = models.FileField(upload_to='resumes', null=False, blank=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications', null=False, blank=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'applications'