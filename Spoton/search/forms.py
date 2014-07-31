from django import forms


from models import Job

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ['site','queueid','state',]

    def __init__(self, *args, **kwargs):
        return super(JobForm, self).__init__(*args, **kwargs)
