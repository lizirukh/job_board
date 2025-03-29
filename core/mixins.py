from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden

class AddVacancyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm('core.add_vacancy'):
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden('You do not have permission to add vacancy.')