from django.shortcuts import render

def index(request):
    return render(request, 'homepage/home.html')

def apps(request):
    return render(request, 'temptext.html', {'message':  "<h1>uhh too lazy to reupload</h1>"})

def developers(request):
    return render(request, 'temptext.html', {'message':  "<a href='https://github.com/svenbaertschi/cambr1dge' class='link-dark'>github (help here)</a>"})

def contact(request):
    return render(request, 'temptext.html', {'message':  "<a href='mailto:will@ubctacs.org' class='link-dark'>will@ubctacs.org</a>"})