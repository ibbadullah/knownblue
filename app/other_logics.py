from usersection.models import *
from adminsection.models import *


# Login check (Allowing only registered users to use the system)
def loginCheck(request):
    if request.user.is_authenticated:
        return True
    else:
        return False



# Email duplicate checking function
def checkEmail(request,email):
    email = email.lower()
    if SignUpModel.objects.filter(email=email).exists():
        return True
    else:
        return False


# Checking admin (This function actually finding that the logged in user is admin or a general user)
def checkAdmin(request):
    if request.user.is_admin == True and request.user.is_staff == True and request.user.is_superuser == True:
        return True
    else:
        return False


# Admin Notification function
def notifyAdmin(request,title,message):
    query = NotificationModel(title=title,message=message)
    return query.save()



