from .models import *
from usersection.models import *
from app.models import *


# Total dictionary
def totalsDic(request):
    totalUsers = SignUpModel.objects.all().count()
    totalArticles = ArticlesModel.objects.all().count()
    totalCategories = CategoryModel.objects.all().count()
    unreadNotifications = NotificationModel.objects.filter(status="Unread").count()
    totalNotifications = NotificationModel.objects.all().count()
    return {"TotalUsers":totalUsers,"TotalNotifications":totalNotifications,
            "TotalArticles":totalArticles,"UnreadNotifications":unreadNotifications,"TotalCategories":totalCategories}


# Data dictionary
def dataDic(request):
    users = SignUpModel.objects.all().order_by("-id")
    articles = ArticlesModel.objects.all().order_by("-id")
    categories = CategoryModel.objects.all()
    allNotifications = NotificationModel.objects.all().order_by("-id")
    allMessages = ContactUsModel.objects.all().order_by("-id")
    chemistryArticles = ArticlesModel.objects.filter(Category__category_name="Chemistry")
    bioArticles = ArticlesModel.objects.filter(Category__category_name="Biology")
    return {"Users": users,"ChemistryArticles":chemistryArticles,"BioArticles":bioArticles,
            "Articles": articles,"AllNotifications":allNotifications,"AllMessages":allMessages,"Categories":categories}



