from django.shortcuts import render
import markdown2
from . import util
from random import choice
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

#================================ FORM FIELD ===================================

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Query', 'class': 'form-control mx-1 my-1'}))

class NewEntryForm(forms.Form):
    new_title = forms.CharField(label="Enter Title", widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control my-1'}))
    new_content = forms.CharField(label="Enter Markdown Content", widget=forms.TextInput(attrs={'placeholder': 'Content', 'class': 'form-control my-1'}))
    

class EditEntryForm(forms.Form):
    # hidden input
    edit_title = forms.CharField(widget=forms.HiddenInput())
    # textarea
    edit_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control my-1'}), label="Edit Content")

#=================================================================================


# list all the entries in encyclopedia
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


# display the content of encyclopedia entry by title
def entry(request, title):
    content = util.get_entry(title)

    # If title not exist, display error page
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

    # convert markdown into html using markdown2
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content),
        "form": SearchForm()
    })

# search encyclopedia entry
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        results = []
        
        # check for form validity
        if form.is_valid():
            query = form.cleaned_data["query"]
            entries_list = util.list_entries()
            
            for entry in entries_list:
                # if query match the encyclopedia entry, display the content
                if query.lower() == entry.lower():
                    title = entry
                    content = util.get_entry(title)
                    return HttpResponseRedirect(reverse("entry", args=[title]))
            
                # query that match partially with entry
                elif query.lower() in entry.lower():
                    results.append(entry)
                    
            return render(request, "encyclopedia/search.html", {
                "results": results,
                "form": SearchForm()
            })
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


# create new entry page
def create(request):

    if request.method == "POST":
        # get the form submitted through POST
        form = NewEntryForm(request.POST)

        if form.is_valid():
            # retrieve data in the form
            title_to_save = form.cleaned_data["new_title"]
            content_to_save = form.cleaned_data["new_content"]
            
            # Ensure no entry page of same title is saved
            entries_list = util.list_entries()
            if title_to_save in entries_list:
                return render(request, "encyclopedia/error.html")

            util.save_entry(title_to_save, content_to_save)
            return HttpResponseRedirect(f"wiki/{title_to_save}") 

        # if the form is not vaild, return form to user together with original input
        return render(request, "encyclopedia/create.html", {
            "create_form": form
        })

    return render(request, "encyclopedia/create.html", {
        "create_form": NewEntryForm()
    })


def edit(request, title):
    markdown_content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "edit_form": EditEntryForm(initial={"edit_title": title, "edit_content": markdown_content})
    })


def saveEdit(request):
    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            title_to_save = form.cleaned_data["edit_title"]
            content_to_save = form.cleaned_data["edit_content"]

            util.save_entry(title_to_save, content_to_save)
            return HttpResponseRedirect(f"wiki/{title_to_save}")


# take user to a random encyclopedia entry
def random(request):
    entries = util.list_entries()

    random_title = choice(entries)
    random_content = util.get_entry(random_title)

    return render(request, "encyclopedia/entry.html", {
        "title": random_title,
        "content": markdown2.markdown(random_content)
    })