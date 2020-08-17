from django.shortcuts import render

def about(request):

    return render(request,'learnit/about-us.html')

def contact(request):

    if request.method == 'POST':
        pass

    return render(request,'learnit/contact-us.html')




