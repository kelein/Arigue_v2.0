from django import forms

# Define UserForm model
class UserForm(forms.Form):
	username = forms.CharField(
		required = True,
		error_messages = {'required': u'Please input username.'},
		widget = forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Username'
		})
	)
	# username = forms.CharField(widget=forms.TextInput)
	password = forms.CharField(
        required = True,
		error_messages = {'required': u'Please input password.'},
		widget = forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': 'Password'
		})
	)


# Define ChpwdForm Model
class PwdForm(forms.Form):
	oldPwd = forms.CharField(
		required = True,
		label = u"Old Password",
		error_messages = {'required': u'Please input old password.'},
		widget = forms.PasswordInput(attrs = {
			'placeholder': 'Old-Password',
		}),
	)

	newPwd = forms.CharField(
		required = True,
		label = u"New Passwrd",
		error_messages = {'required': u'Please input new password.'},
		widget = forms.PasswordInput(attrs = {
			'placeholder': 'New-Password',
		}),
	)

	rePwd = forms.CharField(
		required = True,
		label = u"Re Passwrd",
		error_messages = {'required': u'Please input new password again.'},
		widget = forms.PasswordInput(attrs = {
			'placeholder': 'New-Password',
		}),
	)
	
	def clean(self):
		if not self.is_valid():
			raise forms.ValidationError(u"Please input all items.")
		elif self.cleaned_data['newPwd'] <> self.cleaned_data['rePwd']:
			raise forms.ValidationError(u"Confirm your password.")
		else:
			cleaned_data = super(ChpwdForm, self).clean()
		return cleaned_data

