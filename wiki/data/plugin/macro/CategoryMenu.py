# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - CategoryMenu Macro

    @copyright: 2008, 2009 by Paul Boddie <paul@boddie.org.uk>
    @copyright: 2000-2004 Juergen Hermann <jh@web.de>,
                2005-2008 MoinMoin:ThomasWaldmann.
    @license: GNU GPL (v2 or later), see COPYING.txt for details.
"""

from MoinMoin.Page import Page
from MoinMoin import wikiutil, search, version
import re

__version__ = "0.3"

Dependencies = ['pages']

# Regular expressions where MoinMoin does not provide the required support.

category_regexp = None

# From MoinMoin.search.queryparser...

category_membership_regexp_str = r'(?m)(^-----*\s*\r?\n)(^##.*\r?\n)*^(?!##)(.*)\b%s\b'

# Utility functions.

def isMoin15():
    return version.release.startswith("1.5.")

def getCategoryPattern(request):
    global category_regexp

    try:
        return request.cfg.cache.page_category_regexact
    except AttributeError:

        # Use regular expression from MoinMoin 1.7.1 otherwise.

        if category_regexp is None:
            category_regexp = re.compile(u'^%s$' % ur'(?P<all>Category(?P<key>(?!Template)\S+))', re.UNICODE)
        return category_regexp

# The main activity functions.

def getCategories(request):

    """
    From the AdvancedSearch macro, return a list of category page names using
    the given 'request'.
    """

    # This will return all pages with "Category" in the title.

    cat_filter = getCategoryPattern(request).search
    return request.rootpage.getPageList(filter=cat_filter)

def getCategoryMapping(category_pagenames, request):

    """
    For the given 'category_pagenames' return a list of tuples of the form
    (category name, category page name) using the given 'request'.
    """

    cat_pattern = getCategoryPattern(request)
    mapping = []
    for pagename in category_pagenames:
        name = cat_pattern.match(pagename).group("key")
        if name != "Category":
            mapping.append((name, pagename))
    mapping.sort()
    return mapping

def getPages(pagename, request):

    "Return the links minus category links for 'pagename' using the 'request'."

    query = search.QueryParser().parse_query('category:%s' % pagename)
    if isMoin15():
        results = search.searchPages(request, query)
        results.sortByPagename()
    else:
        results = search.searchPages(request, query, "page_name")

    cat_pattern = getCategoryPattern(request)
    pages = []
    for page in results.hits:
        if not cat_pattern.match(page.page_name):
            pages.append(page)
    return pages

def getPrettyPageName(page):

    "Return a nicely formatted title/name for the given 'page'."

    if isMoin15():
        title = page.split_title(page.request, force=1)
    else:
        title = page.split_title(force=1)

    return title.replace("_", " ").replace("/", u" ?")

def linkToPage(request, page, text, query_string=None):

    """
    Using 'request', return a link to 'page' with the given link 'text' and
    optional 'query_string'.
    """

    text = wikiutil.escape(text)

    if isMoin15():
        url = wikiutil.quoteWikinameURL(page.page_name)
        if query_string is not None:
            url = "%s?%s" % (url, query_string)
        return wikiutil.link_tag(request, url, text, getattr(page, "formatter", None))
    else:
        return page.link_to_raw(request, text, query_string)

def execute(macro, args):

    """
    Execute the 'macro' with the given 'args': an optional list of selected
    category names (categories whose pages are to be shown).
    """

    request = macro.request
    fmt = macro.formatter
    page = fmt.page

    # Interpret the arguments.

    try:
        selected_category_names = args and wikiutil.parse_quoted_separated(args, name_value=False) or []
    except AttributeError:
        selected_category_names = args.split(",")

    selected_category_names = [arg for arg in selected_category_names if arg]

    # Get the categories.

    categories = getCategoryMapping(getCategories(request), request)

    # Generate a menu with the categories, together with expanded submenus for
    # the categories employed by the current page, the category represented by
    # the current page, or for those categories specified in the macro
    # arguments.

    output = []
    output.append(fmt.bullet_list(on=1, attr={"class" : "category-menu"}))

    for category in categories:
        category_name, category_pagename = category

        # Work out whether the current page belongs to this category.

        page_is_category = page.page_name == category_pagename
        category_membership_regexp = re.compile(category_membership_regexp_str % category_pagename)
        page_is_in_category = category_membership_regexp.search(page.get_raw_body())

        # Generate the submenu where appropriate.

        if selected_category_names and category_name in selected_category_names or \
            not selected_category_names and (page_is_category or page_is_in_category):

            if page_is_category:
                output.append(fmt.listitem(on=1, attr={"class" : "selected current"}))
                output.append(fmt.text(category_name))
            else:
                output.append(fmt.listitem(on=1, attr={"class" : "selected"}))
                output.append(fmt.pagelink(on=1, pagename=category_pagename))
                output.append(fmt.text(category_name))
                output.append(fmt.pagelink(on=0, pagename=category_pagename))

            output.append(fmt.bullet_list(on=1, attr={"class" : "category-submenu"}))

            # Get the pages and page names in the category.

            pages_in_category = getPages(category_pagename, request)

            # Visit each page in the category.

            last_parts = []

            for page_in_category in pages_in_category:
                pagename = page_in_category.page_name

                # Get a real page, not a result page.

                real_page_in_category = Page(request, pagename)

                # Get a pretty version of the page name.

                pretty_pagename = getPrettyPageName(real_page_in_category)

                if page.page_name == pagename:
                    output.append(fmt.listitem(on=1, attr={"class" : "selected"}))
                else:
                    output.append(fmt.listitem(on=1))

                # Abbreviate long hierarchical names.

                parts = pretty_pagename.split(u" ?")
                common = 0
                for last, current in map(None, last_parts, parts):
                    if last == current:
                        common += 1
                    else:
                        break

                # Use the arrows to indicate subpages.

                prefix = u" ?" * common
                suffix = u" ?".join(parts[common:])

                output.append(fmt.text(prefix))

                # Link to the page using the pretty name.

                output.append(linkToPage(request, real_page_in_category, suffix))
                output.append(fmt.listitem(on=0))

                last_parts = parts

            output.append(fmt.bullet_list(on=0))
            output.append(fmt.listitem(on=0))

        # Otherwise generate a simple link.

        else:
            output.append(fmt.listitem(on=1))
            output.append(fmt.pagelink(on=1, pagename=category_pagename))
            output.append(fmt.text(category_name))
            output.append(fmt.pagelink(on=0, pagename=category_pagename))
            output.append(fmt.listitem(on=0))

    output.append(fmt.bullet_list(on=0))

    return ''.join(output)

# vim: tabstop=4 expandtab shiftwidth=4
