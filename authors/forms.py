from django import forms

from authors.models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'birthday')

    def __init__(self, *args, validate_unique_author=None, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self._validate_unique_author = validate_unique_author

    def clean(self):
        cleaned_data = super(AuthorForm, self).clean()
        if self._validate_unique_author and not self.errors:
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            birthday = self.cleaned_data['birthday']
            self._validate_unique_author(first_name=first_name, last_name=last_name, birthday=birthday)
        return cleaned_data
