from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import re
from django import forms 
import random

def search(request):
    if request.method == 'GET' and request.GET.get('q') is not None:
        query= request.GET.get('q')
        if query in util.list_entries():
            return HttpResponseRedirect(reverse("wiki:getEntry", kwargs={'entryName': query }))
        else:
            matchSearchEntries = []
            for entryName in util.list_entries():
                x = re.findall(query, entryName)
                if x:
                    matchSearchEntries += [entryName]
            if len(matchSearchEntries) != 0:
                return render(request, 'encyclopedia/search.html', {"entries": matchSearchEntries})
            else:
                return HttpResponseRedirect(reverse("wiki:getEntry", kwargs={'entryName': query }))
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})

def index(request):    
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def getEntry(request, entryName):
    context = {
        'entryName': entryName,
        'entries': util.get_entry(entryName),
        }
    if entryName not in util.list_entries():
        context = {
        'entryName': "Not Found",
        'entries': "The entry could not be found.",
        }
        return render(request, 'encyclopedia/errorentry.html', context)
    else:
        return render(request, 'encyclopedia/entry.html', context)


def createPage(request):
    if request.method == "POST":
        title = request.POST.get('title') 
        entryContent = request.POST.get('content') 
        if title in util.list_entries():
            context = {
            'entryName': "Error",
            'entries': "Entry already exists",
            }
            return render(request, 'encyclopedia/errorentry.html', context)
        else:
            util.save_entry(title, entryContent)
            return HttpResponseRedirect(reverse("wiki:getEntry", kwargs={'entryName': title}))
    return render(request, 'encyclopedia/createPage.html')

def editPage(request):
    title = request.POST.get('title') 
    context = {
        'title': title,
        'content': util.get_entry(title),
    }
    return render(request,'encyclopedia/editPage.html',context)

def saveEditedPage(request):
    if request.method == "POST": 
        util.save_entry(request.POST.get('title'), request.POST.get('content'))
        return HttpResponseRedirect(reverse("wiki:getEntry", kwargs={'entryName': request.POST.get('title')}))

def randomPage(request):
    return HttpResponseRedirect(reverse("wiki:getEntry", kwargs={'entryName': random.choice(util.list_entries())}))
