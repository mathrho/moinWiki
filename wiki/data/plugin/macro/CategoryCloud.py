# -*- coding: iso-8859-1 -*-
u"""
    MoinMoin - CategoryCloud macro Version 0.3.2 BETA
               Output a tag cloud of categry pages

    @copyright: 2009 by MarcelHäfner (http://moinmo.in/MarcelHäfner)
                (this code is a bigger rewrite of the macro TagCloud by Christian Groh)
                2010 Krzysztof Stryjek: Optimized the Category Stuff and added tagSplit parameter
                2011  RyoSato:  Optimized the regex stuff
                
    @license: GNU GPL, see COPYING for details.

    @TODO:
    The final output should be optimized and not using that much code and
        style stuff

"""

from MoinMoin.Page import Page
import re

#Dependencies = ["namespace"] #use this, if you not like to use caching
Dependencies = []


def macro_CategoryCloud(macro, maxTags=30, fontSize=0.65, categoryKey=ur'Category', tagSplit=','):

    #inital stuff
    request = macro.request
    fmt = macro.formatter
    _ = request.getText
    errorMsg = []
    html = []
    tags = []
    taglist = []
    show = []
    #{level:hits , level:hits , ...}
    level = {0: 4, 1: 7, 2: 12, 3: 18, 4: 25, 5: 35, 6: 50, 7: 60, 8: 90}

    #fetch all pages, except underlays
    pages = request.rootpage.getPageList(exists=1, include_underlay=False, )
    if not pages:
        errorMsg.append(fmt.div(True, css_class="error"))
        errorMsg.append(_("No pages exist or you have not enough rights to view them"))
        errorMsg.append(fmt.div(False))
        return ''.join(errorMsg)

    #find CategoryFoo tags and count them
    for page in pages:
        page = Page(request, page)
        if page.isStandardPage() and not page.isUnderlayPage():
            body = page.get_raw_body()
            match = re.search(ur'(?m)(^-----*\s*\r?\n)(^##.*\r?\n)*^(?!##)(.*)(?P<all>' + categoryKey + ur'(?P<category>[^ \s\]]+))', body)
            if match == None:
                continue
            match = match.group('category')
            match = match.split(tagSplit)
            for tag in match:
                tags.insert(0, (str(tag.encode('utf8'))).strip())
    taglist = list(frozenset(tags))

    #sorting the taglist and output as show
    def sort(t):
        return t[1]

    for tag in taglist:
        show.append((tag, tags.count(tag)))
    show.sort(key=sort, reverse=True)
    show = show[0:maxTags]
    show.sort()

    #generate the cloud. TODO: code should be optimized
    html.append(fmt.div(True, css_class="PageCloud", style="display:inline;"))
    for tag in show:
        pagename = categoryKey + tag[0].decode('utf8')
        hits = tag[1]
         #level0
        if hits < level[0]:
            html.append(fmt.span(True, style="font-size:%sem;") % fontSize)
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level1
        elif hits < level[1]:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 0.15))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level2
        elif hits < level[2]:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 0.25))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level3
        elif hits < level[3]:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 0.35))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level4
        elif hits < level[4]:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 0.45))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level5
        elif hits < level[5]:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 0.55))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level6
        elif hits < level[6]:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 0.65))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level7
        elif hits < level[7]:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 0.75))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level8
        elif hits < level[8]:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 0.85))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))
        #level9
        else:
            html.append(fmt.span(True, style="font-size:%sem;") % str(fontSize + 1.05))
            html.append(fmt.pagelink(True, pagename))
            html.append(fmt.text(tag[0].decode('utf8')))
            html.append(fmt.pagelink(False))
            html.append(fmt.span(False))
            html.append(fmt.text(" "))

    #output
    html.append(fmt.div(False))
    return ''.join(html)
