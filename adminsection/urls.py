from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required



urlpatterns = [
    # Admin dashboard related url
    path('a/dashboard/', adminDashboardView, name="AdminDashboard"),

    # Admin account related urls
    path('a/180.1.1/',AdminLoginView.as_view(),name="AdminLoginView"),
    path('a/admin-logout/',adminLogout,name="AdminLogout"),
    path('a/profile/',showAdminProfile,name="AdminProfileInfo"),
    path('a/update-profile/',login_required(AdminProfileUpdateView.as_view()),name="AdminProfileUpdateView"),

    # Categories related urls
    path('a/add-category/',login_required(AddCategoryView.as_view()),name="AddCategory"),
    path('a/all-categories/',showCategoriesView,name="AllCategories"),
    path('a/del-category/<int:id>/',deleteCategoryView,name="DeleteCategory"),
    path('a/update-category/<int:id>/',login_required(CategoryUpdateView.as_view()),name="UpdateCategory"),

    # Articles related urls
    path('a/add-article/',login_required(AddArticleView.as_view()),name="AddArticle"),
    path('a/all-articles/',showArticlesView,name="AllArticles"),
    path('a/del-article/<int:id>/',deleteArticleView,name="DeleteArticle"),
    path('a/update-article/<int:id>/',ArticleUpdateView.as_view(),name="UpdateArticle"),


    # Approved users related urls
    path('a/approved-users/',showApprovedUsersView,name="ApprovedUsers"),
    path('a/del-ap-user/<int:id>/',deleteApprovedUser,name="DeleteApprovedUser"),
    path('a/user-update-admin/<int:id>/',login_required(UserProfileUpdateViewAdmin.as_view()),name="UserProfileUpdateViewAdmin"),

    # Notifications related urls
    path('a/all-notifications/',showAllNotificationsView,name="AllNotifications"),
    path('a/notification/<int:id>/',notificationDetailsView,name="SingleNotification"),
    path('a/del-notification/<int:id>/', delnotificationView, name="DeleteNotification"),

    # Views related urls
    path('a/all-messages/',showAllMessages,name="AllMessages"),
    path('a/del-m/<int:id>/', delMessage, name="DeleteMessage"),

]
