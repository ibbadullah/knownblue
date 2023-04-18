from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.views import View
from django.contrib import messages
from app.other_logics import *
from django.contrib.auth.decorators import login_required
from .models import *
from app.models import *



'''
#########################################
Admin account related views
#########################################
'''
# Class base view for admin login
class AdminLoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("AdminDashboard")
        else:
            return render(request,"adminsection/admin-login.html")

    def post(self,request):
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            # First checking the user (if the user is admin then we want to allow him to login through the admin login area)
            if SignUpModel.objects.filter(email=email,is_staff=True,is_admin=True,is_superuser=True).exists():
                user = authenticate(email=email,password=password)
                if user is not None:
                    login(request,user)
                    return redirect("AdminDashboard")
                else:
                    messages.info(request,"Sorry, your email or password is incorrect.")
                    return redirect("AdminLoginView")
            else:
                messages.info(request, "Sorry, you're not an admin. You can't access the sensitive area of Doc2Vec application.")
                return redirect("AdminLoginView")


# View for showing admin profile info
@login_required(login_url="AdminLoginView")
def showAdminProfile(request):
    if checkAdmin(request) == True:
        return render(request, "adminsection/profile-info.html")
    else:
        return render(request, '404.html')


# Class base view for updating the admin profile
class AdminProfileUpdateView(View):
    def get(self,request):
        if checkAdmin(request) == True:
            return render(request, "adminsection/admin-update-profile.html")
        else:
            return render(request, '404.html')

    def post(self,request):
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]
        email = request.POST["email"].lower()
        # Matching user db email and profile form email (If it matched then it means admin is just changing their name)
        if request.user.email == email:
            # Getting logged in admin record by id
            query = SignUpModel.objects.get(id=request.user.id)
            query.first_name = firstName
            query.last_name = lastName
            query.save()
            messages.info(request,"Your account has been updated successfully.")
            return redirect("AdminProfileUpdateView")
        # Checking user email for duplication
        elif SignUpModel.objects.filter(email=email).exists():
            m = "Sorry, an account is already created on the current email. Please use another one."
            messages.info(request,m)
            return redirect("AdminProfileUpdateView")

        else:
            query = SignUpModel.objects.get(id=request.user.id)
            query.first_name = firstName
            query.last_name = lastName
            query.email = email
            query.save()
            messages.info(request, "Your account has been updated successfully with new email.")
            return redirect("AdminProfileUpdateView")



# Admin dashboard view
@login_required(login_url="AdminLoginView")
def adminDashboardView(request):
    # Checking if the request is from any admin then allowing to admin dashboard otherwise
    # landing request on 404 page which is the best place for none admins
    if checkAdmin(request) == True:
        return render(request,"adminsection/dashboard.html")
    else:
        return render(request,'404.html')


# Admin logout view
def adminLogout(request):
    logout(request)
    messages.info(request,"You have successfully logged out from the system. Thanks for working with Doc2Vec.")
    return redirect("AdminLoginView")





'''
#########################################
Category related views
#########################################
'''

# class base view for add category
class AddCategoryView(View):
    def get(self,request):
        if checkAdmin(request) == True:
            return render(request, "adminsection/add-category.html")
        else:
            return render(request, '404.html')

    def post(self,request):
        if checkAdmin(request) == True:
            c_name = request.POST["category_name"]
            c_author = request.POST["category_author"]
            c_keywords = request.POST["category_keywords"]
            c_description = request.POST["category_description"]
            query = CategoryModel(category_name=c_name,category_description=c_description,category_author=c_author,
                                  category_keywords=c_keywords)
            query.save()
            messages.info(request, "A new category has been added successfully!")
            return redirect("AllCategories")
        else:
            return render(request, '404.html')


# all categories show view
@login_required(login_url="AdminLoginView")
def showCategoriesView(request):
    if checkAdmin(request) == True:
        query = CategoryModel.objects.all().order_by("-id")
        return render(request, "adminsection/all-categories.html",{"Categories":query})
    else:
        return render(request, '404.html')


# class base view for category update
class CategoryUpdateView(View):
    def get(self,request,id):
        try:
            if checkAdmin(request) == True:
                query = CategoryModel.objects.get(id=id)
                return render(request, "adminsection/update-category.html", {"Category": query})
            else:
                return render(request, "404.html")
        except:
            messages.info(request, "Something went wrong.")
            return redirect("AllCategories")



    def post(self,request, id):
        try:
            if request.method == "POST":
                if checkAdmin(request) == True:
                    c_name = request.POST["category_name"]
                    c_description = request.POST["category_description"]
                    c_author = request.POST["category_author"]
                    c_keywords = request.POST["category_keywords"]
                    query = CategoryModel.objects.get(id=id)
                    query.category_name = c_name
                    query.category_description = c_description
                    query.category_author = c_author
                    query.category_keywords = c_keywords
                    query.save()
                    messages.info(request, "Category has been updated successfully!")
                    return redirect("AllCategories")
                else:
                    return render(request, '404.html')
            else:
                return render(request, '404.html')
        except:
            messages.info(request, "Something went wrong.")
            return redirect("AllCategories")






# delete category view
@login_required(login_url="AdminLoginView")
def deleteCategoryView(request,id):
    try:
        if checkAdmin(request) == True:
            query = CategoryModel.objects.get(id=id)
            query.delete()
            messages.info(request, "Category has been deleted successfully!")
            return redirect("AllCategories")
        else:
            return render(request, '404.html')
    except:
        messages.info(request, "Something went wrong.")
        return redirect("AllCategories")




'''
#########################################
Articles related views
#########################################
'''

# class base view for add article
class AddArticleView(View):
    def get(self,request):
        if checkAdmin(request) == True:
            query = CategoryModel.objects.all()
            return render(request, "adminsection/add-article.html",{"Categories":query})
        else:
            return render(request, '404.html')

    def post(self,request):
        if checkAdmin(request) == True:
            c_id = request.POST["category_id"]
            a_title = request.POST["article_title"]
            a_mt = request.POST["article_meta_des"]
            a_keywords = request.POST["article_keywords"]
            a_author = request.POST["article_author"]
            a_content = request.POST["article_content"]
            a_image = request.FILES["article_image"]
            query = ArticlesModel(Category_id=c_id,article_title=a_title,article_author=a_author,article_content=a_content,
                                  article_image=a_image,article_keywords=a_keywords,artilce_meta_des=a_mt)
            query.save()
            messages.info(request, "A new article has been added successfully!")
            return redirect("AllArticles")
        else:
            return render(request, '404.html')


# all articles show view
@login_required(login_url="AdminLoginView")
def showArticlesView(request):
    if checkAdmin(request) == True:
        query = ArticlesModel.objects.all().order_by("-id")
        return render(request, "adminsection/all-articles.html",{"Articles":query})
    else:
        return render(request, '404.html')


# class base view for article update
class ArticleUpdateView(View):
    def get(self,request,id):
        try:
            if checkAdmin(request) == True:
                query = ArticlesModel.objects.get(id=id)
                category = CategoryModel.objects.all()
                return render(request, "adminsection/update-article.html", {"Article": query,"Categories":category})
            else:
                return render(request, "404.html")
        except:
            messages.info(request, "Something went wrong.")
            return redirect("AllArticles")



    def post(self,request, id):
        try:
            if request.method == "POST":
                if checkAdmin(request) == True:
                    a_category = request.POST["category_id"]
                    a_title = request.POST["article_title"]
                    a_keywords = request.POST["article_keywords"]
                    a_author = request.POST["article_author"]
                    a_content = request.POST["article_content"]
                    a_image = request.FILES["article_image"]
                    a_mt = request.POST["article_meta_des"]
                    query = ArticlesModel.objects.get(id=id)
                    query.Category_id = a_category
                    query.article_title = a_title
                    query.article_keywords = a_keywords
                    query.article_author = a_author
                    query.article_content = a_content
                    query.article_image = a_image
                    query.artilce_meta_des = a_mt
                    query.save()
                    messages.info(request, "The article has been updated successfully.")
                    return redirect("AllArticles")
                else:
                    return render(request, '404.html')
            else:
                return render(request, '404.html')
        except:
            messages.info(request, "Something went wrong.")
            return redirect("AllArticles")



# delete article view
@login_required(login_url="AdminLoginView")
def deleteArticleView(request,id):
    try:
        if checkAdmin(request) == True:
            query = ArticlesModel.objects.get(id=id)
            query.delete()
            messages.info(request, "The article has been deleted successfully!")
            return redirect("AllArticles")
        else:
            return render(request, '404.html')
    except:
        messages.info(request, "Something went wrong.")
        return redirect("AllArticles")






'''
#########################################
Approved users related views
#########################################
'''
# Displaying approved users view
@login_required(login_url="AdminLoginView")
def showApprovedUsersView(request):
    if checkAdmin(request) == True:
        return render(request, "adminsection/approved-users.html")
    else:
        return render(request, '404.html')


# Delete approved user view
@login_required(login_url="AdminLoginView")
def deleteApprovedUser(request,id):
    try:
        if checkAdmin(request) == True:
            # deleting user
            uaUser = SignUpModel.objects.get(id=id)
            uaUser.delete()
            messages.info(request,"The user account has been removed permanently from the system.")
            return redirect("ApprovedUsers")
        else:
            return render(request, '404.html')
    except:
        messages.info(request,"Something went wrong.")
        return redirect('ApprovedUsers')


# Class base view for profile update view
class UserProfileUpdateViewAdmin(View):
    def get(self,request,id):
        try:
            if checkAdmin(request) == True:
                query = SignUpModel.objects.get(id=id)
                return render(request, "adminsection/update-user.html", {"User": query})
            else:
                return render(request, '404.html')
        except:
            return render(request, '404.html')


    def post(self,request,id):
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]
        email = request.POST["email"].lower()
        # Getting username and email from db in order to match with current details
        mQuery = SignUpModel.objects.get(id=id)

        # Matching current form email with db email
        if mQuery.email == email:
            mQuery.first_name = firstName
            mQuery.last_name = lastName
            mQuery.save()
            messages.info(request,"Account updated successfully.")
            return redirect("ApprovedUsers")
        # Checking user email for duplication
        elif SignUpModel.objects.filter(email=email).exists():
            m = "Sorry, an account is already created on the current email. Please use another one."
            messages.info(request,m)
            return redirect("UserProfileUpdateViewAdmin",id)

        else:
            query = SignUpModel.objects.get(id=id)
            query.first_name = firstName
            query.last_name = lastName
            query.email = email
            query.save()
            messages.info(request, "The user account has been updated successfully with a new email.")
            return redirect("ApprovedUsers")


'''
#########################################
All notifications related views
#########################################
'''
# Displaying all notifications view
@login_required(login_url="AdminLoginView")
def showAllNotificationsView(request):
    if checkAdmin(request) == True:
        return render(request, "adminsection/all-notifications.html")
    else:
        return render(request, '404.html')


# view for showing single notification
@login_required(login_url="AdminLoginView")
def notificationDetailsView(request,id):
    try:
        if checkAdmin(request) == True:
            # getting notification & changing the status as well
            query = NotificationModel.objects.get(id=id)
            uQuery = NotificationModel.objects.get(id=id)
            uQuery.status = "Read"
            uQuery.save()
            return render(request, "adminsection/notification-details.html", {"Notification": query})
        else:
            return render(request, '404.html')
    except:
        return render(request, '404.html')


# view for deleting single notification
@login_required(login_url="AdminLoginView")
def delnotificationView(request,id):
    try:
        if checkAdmin(request) == True:
            # deleting notification
            query = NotificationModel.objects.get(id=id)
            query.delete()
            messages.info(request,"The notification has been deleted successfully.")
            return redirect("AllNotifications")
        else:
            return render(request, '404.html')
    except:
        return render(request, '404.html')




'''
#########################################
Messages related stuff
#########################################
'''
# Displaying all messages
@login_required(login_url="AdminLoginView")
def showAllMessages(request):
    if checkAdmin(request) == True:
        return render(request, "adminsection/all-messages.html")
    else:
        return render(request, '404.html')


# view for deleting message
@login_required(login_url="AdminLoginView")
def delMessage(request,id):
    try:
        if checkAdmin(request) == True:
            # deleting message
            query = ContactUsModel.objects.get(id=id)
            query.delete()
            messages.info(request,"The message has been deleted successfully.")
            return redirect("AllMessages")
        else:
            return render(request, '404.html')
    except:
        return render(request, '404.html')
