from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown

import random
import markdown2
import re

markdowner = Markdown()


class newEntryForm(forms.Form):
 title = forms.CharField(label="Enter Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-35 col-lg-35', 'row': 3}))
 content= forms.CharField(label="Enter Content",widget=forms.Textarea(attrs={'class' : 'form-control col-md-10 col-lg-12', 'rows' : 18}))
 
 

def index(request):
    entries = util.list_entries()
    for title in entries:
        title = util.get_entry(title)
    return render(request, "encyclopedia/index.html", {
        "title": title,
        "entries": util.list_entries()
    })

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        entryPage = util.get_entry(title)
        entryPageConvert = markdowner.convert(entryPage)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "entryPage": entryPageConvert
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message1": "Sorry the requested page is not found. Try Again"
        })


def newEntry(request):
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None and util.get_entry(content) is None):
                util.save_entry(title, content)
                entryPage = util.get_entry(title)
                entryPageConvert = markdowner.convert(entryPage)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entryPage": entryPageConvert,
                })
            else:
              return render(request, "encyclopedia/error.html",{
                  "message2": "This page with same title already EXISTS. Please click Home button and check the titles."
              })    
        else:
            return HttpResponseRedirect(reversed, "encyclopedia/newEntry.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": newEntryForm
        })


def edit(request, title):
    entryPage = util.get_entry(title)
    if request.method == 'GET':
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'content': entryPage
        })
    if request.method == 'POST':
        entryPage = request.POST.get('newcontent')
        util.save_entry(title, entryPage)
        entryPageConvert = markdowner.convert(entryPage)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "entryPage": entryPageConvert
        })


def search(request):
    entries = util.list_entries()
    if request.method == 'POST':
        item = request.POST
        item = item['q']
        searchlist = []

        for title in entries:

            if re.search(item.lower(), title.lower()):
                searchlist.append(title)
        if len(searchlist) == 0: 
            return render(request, "encyclopedia/error.html", {
                "message3": "Sorry. No results found based on your Search. Please Try Again"
            })

    return render(request, "encyclopedia/search.html", {
        'entries': searchlist
    })

def random_pages(request):
    entries = util.list_entries()
    random_entry = random.randint(0, len(entries)-1)
    title = entries[random_entry]
    entryPage = util.get_entry(title)
    entryPageConvert= markdowner.convert(entryPage)
    return render(request, "encyclopedia/entry.html",{
        'title': title,
        'entryPage': entryPageConvert
    })



        

        
