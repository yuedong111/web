from django.shortcuts import render,HttpResponse
from register.forms import RegisterForm
from hashlib import md5
# Create your views here.


def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			try:
				new_form = form.save(commit=False)
				m = md5()
				m.update((email+password).encode('utf-8'))
				new_form.password = m.hexdigest()
				new_form.save()
				form.save_m2m()
			except:
				return HttpResponse('糟糕，注册失败')
			return HttpResponse('恭喜，注册成功')
	form = RegisterForm()
	return render(request, 'register.html', {'form': form})