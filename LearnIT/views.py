from django.shortcuts import render

def about(request):
    context={}
    context['about_nav'] = 'active'
    return render(request,'learnit/about-us.html',context=context)

def contact(request):
    context={}
    context['contact_nav'] = 'active'
    if request.method == 'POST':
        pass

    return render(request,'learnit/contact-us.html',context=context)




