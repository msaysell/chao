from django import forms
from django.core.mail import send_mail
from Darts import settings


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ContactForm(BootstrapForm):
    CATEGORY_COMPLAINT = 'Complaints or Issues'
    CATEGORY_WEBSITE = 'Website problems'
    CATEGORY_QUERIES = 'All other queries'
    CATEGORIES = ((CATEGORY_COMPLAINT, CATEGORY_COMPLAINT),
                  (CATEGORY_WEBSITE, CATEGORY_WEBSITE),
                  (CATEGORY_QUERIES, CATEGORY_QUERIES),
                  )
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True, max_length=256)
    category = forms.ChoiceField(required=True, choices=CATEGORIES)
    content = forms.CharField(required=True, widget=forms.Textarea)

    def send_email(self):

        recipients = {self.CATEGORY_COMPLAINT: 'pubandclubtuesdaydarts@outlook.com',
                      self.CATEGORY_WEBSITE: 'mike@saysell.net',
                      self.CATEGORY_QUERIES: 'steverobinson316@ntlworld.com'}

        send_mail(subject=self.cleaned_data['subject'],
                  message=self.cleaned_data['content'],
                  from_email=self.cleaned_data['email'],
                  recipient_list=[recipients.get(self.cleaned_data['category'], settings.DEFAULT_FROM_EMAIL)],
                  fail_silently=True)


class AddPlayerForm(BootstrapForm):
    players = forms.CharField(widget=forms.Textarea)


class FixtureCreator(BootstrapForm):
    number_of_teams = forms.IntegerField(label='Number of Teams')
    times_to_play = forms.IntegerField(label='Times to play each other')
