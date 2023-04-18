from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .other_logics import *
from .models import ContactUsModel
from django.core.paginator import Paginator


# Home view
def HomeView(request):
    return render(request,'publicsection/index.html')


# Class based view for contact us
class ContactUsView(View):
    def get(self,request):
        return render(request,'publicsection/contact.html')

    def post(self,request):
        if request.method == "POST":
            fullName = request.POST['full_name']
            email = request.POST['email']
            message = request.POST['message']
            query = ContactUsModel(full_name=fullName,email=email,message=message)
            query.save()
            if query:
                # notifying admin about the message
                title = "A new message received"
                mText = "A new message has received from "+fullName+". Please read the message & give a response to the user."
                notifyAdmin(request,title,mText)
                m = "Thank you for your message. We received your message. We will respond to you as soon as possible."
                return render(request,"publicsection/contact.html",{"Message":m})
            else:
                m = "Sorry, something went wrong."
                return render(request, "publicsection/contact.html", {"Message": m})



def categoryArticles(request,slug):
    try:
        query = ArticlesModel.objects.filter(Category__category_slug=slug)
        paginator = Paginator(query,9)
        page = request.GET.get('page')
        query = paginator.get_page(page)
        category = CategoryModel.objects.get(category_slug=slug)
        return render(request, 'publicsection/category_articles.html', {"Data": query,"C":category})
    except:
        return render(request,'404.html')
