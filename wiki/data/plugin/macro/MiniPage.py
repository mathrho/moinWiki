# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - MiniPage Macro
    
    This macro is used to write multi line markup into a table. 
    Add a linefeed for a new line e.g.
    ||Buttons ||<<MiniPage( * Redo\n * Undo)>><<MiniPage( * Quit)>>||
    ||Section ||<<MiniPage(= heading 1 =)>><<MiniPage(== heading 2 ==)>>||
        
    @copyright: 2005-2012 by MoinMoin:ReimarBauer
    @license: GNU GPL, see COPYING for details.
"""
from MoinMoin import wikiutil

def execute(macro, text):
     request = macro.request
     text = ''.join(text)
     text = text.replace('\\n', '\n')
     Parser = wikiutil.searchAndImportPlugin(request.cfg, "parser", request.page.pi['format'])
     return wikiutil.renderText(request, Parser, text)

