__author__ = 'ironeagle'

from django import forms


class SignatureForm(forms.Form):

    def __init__(self, signature,  *args, **kwargs):
        super(SignatureForm, self).__init__(*args, **kwargs)
        for component in signature.components:
            self.fields["component_%s" % component] = forms.CharField()

    def save(self):
        print ">>>>self.cleaned_data"
        print self.cleaned_data
        return {'success': True, 'message': 'this is message from form'}