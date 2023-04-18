from django.shortcuts import render,redirect
from app.other_logics import *
from django.db.models import Q


# Article search view
def articleSearchView(request):
    try:
        if request.method == "GET":
            q = request.GET['q']
            # getting data
            query = ArticlesModel.objects.filter(Q(article_title__icontains=q)|Q(article_keywords__icontains=q))
            if query:
                return render(request, "publicsection/search_page.html", {"Data": query})
            else:
                m = "Sorry, no results found for your query."
                return render(request, "publicsection/search_page.html", {"Message": m})
    except:
        return render(request,"404.html")



# Single article
def getSingleArticle(request,categ_slug,article_slug):
    try:
        query = ArticlesModel.objects.get(Category__category_slug=categ_slug, article_slug=article_slug)
        # calling related articles slug
        relatedArticles = getRelatedArticles(request,categ_slug,article_slug)
        return render(request, "publicsection/article_details.html", {"A": query,"RelatedArticles":relatedArticles})
    except:
        return render(request,"404.html")



# view for returning related articles for the same category
def getRelatedArticles(request,c_slug,a_slug):
    try:
        query = ArticlesModel.objects.filter(Category__category_slug=c_slug).exclude(article_slug=a_slug).order_by("-id")
        return query
    except:
        pass


