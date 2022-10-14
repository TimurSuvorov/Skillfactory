from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerPermissionRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        if self.request.user != 'admin' and self.request.user.id != self.get_object().postAuthor.author.id:  # id для сравнения берется из модели User
            raise PermissionDenied()
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)
