from django.shortcuts import render,HttpResponse


def appmain(request):
	# write your python code!!
	return render(request, 'app_13/main.html',{
		'test' : '草',
		'test2' : '不可避',
	})