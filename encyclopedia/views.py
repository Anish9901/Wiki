from ctypes import sizeof
from django.shortcuts import redirect, render
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, titles):
    return render(request, "wiki/entry.html", {
        "titles": util.get_entry(titles),
        "name": titles,
    })


def search(request):
    a = request.get_full_path()
    x = "?q="

    if(a.find(x) != -1):
        b = a.index("=")
        a = a[b+1:]
        b = a
    a = a.lower()
    outlist = []
    items = util.list_entries()
    items_copy = items.copy()

    for i in range(len(items)):
        items[i] = items[i].lower()
    for i in items:
        if a in i:
            outlist.append(items_copy[items.index(i)])

    if a in items:
        i = items.index(a)
        return entry_page(request, items_copy[i])
    elif len(outlist) > 0:
        return render(request, "encyclopedia/index.html", {
            "entries": outlist,
            "search": 1
        })
    else:
        return entry_page(request, a)


def create_newpage(request):
    items = util.list_entries()

    for i in range(len(items)):
        items[i] = items[i].lower()

    title_name = ''
    content_text = ''

    if request.method == 'POST':
        # ['title'] and ['content'] are textarea fields in new.html
        title_name = request.POST['title']
        content_text = "# "+ title_name + "\n\n" + request.POST['content']
    
    a = title_name.lower()
    if a in items:
        return render(request,"wiki/new.html", {
            "errorcode": 1,
            "name": title_name
        })
    elif a not in items and title_name != '':
        util.save_entry(title_name,content_text)
        return entry_page(request,title_name)
    return render(request, "wiki/new.html")


def edit_page(request,page_name): 
    var = util.get_entry_for_edit(page_name)
    i = 2 # i = 2 for '# '
    t = ""
    c = ""
    
    #t gets the title
    while(var[i]!='\n'):
        t = t + var[i]
        i+=1

    #for striping whitespace
    while(var[i].isspace()):
        i += 1
    c = var[i:]

    title_name = ''
    content_text = ''

    if request.method == 'POST':
        # ['title'] and ['content'] are textarea fields in new.html
        title_name = request.POST['title']
        content_text = "# "+ title_name + "\n\n" + request.POST['content']
        util.save_entry(title_name,content_text)
        return entry_page(request,title_name)
    # the bottom return is activated first and then after click the above if statement becomes true and the edited page is saved and displayed.
    return render(request,"wiki/edit.html",{
        "title": t,
        "content": c,
    })


def random_page(request):
    i = 0
    items = util.list_entries()
    i = random.randint(0, len(items)-1)
    return entry_page(request, items[i])
