from django import forms
from django.utils.functional import lazy

from news.extension import COUNTRIES
from news.models import UserInfo

from allauth.account.forms import SignupForm, PasswordField
from django.utils.translation import gettext, gettext_lazy as _, pgettext
gettext_lazy = lazy(gettext, str)
pgettext_lazy = lazy(pgettext, str)


class CustomSignUpFromallauth(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignUpFromallauth, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=64,
                                                    label='First Name',
                                                    required=True
                                                    )
        self.fields['country'] = forms.ChoiceField(label='Country',
                                                   choices=COUNTRIES,
                                                   )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        country = self.cleaned_data.pop('country')
        UserInfo.objects.create(country=country, user=user)
        user.save()
        return user

