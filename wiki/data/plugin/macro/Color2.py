"""
    MoinMoin - Color2 Macro

    @copyright: 2006 by Clif Kussmaul <clif@kussmaul.org>
                2008 by Clif Kussmaul, Dave Hein (MoinMoin:DaveHein)
                2011 by Clif Kussmaul, Dave Hein (MoinMoin:DaveHein), Gregor Mirai
    @license:   GNU GPL, see COPYING for details

    Usage: <<Color2(text,col=color,bcol=bgcolor,font=_font_)>>
           <<Color2(text,bcol=bgcolor)>>
           <<Color2(text,color)>>

    History:
    - 2011.02.23: [Moin 1.9] updated for Moin 1.9 by Gregor Mirai,
                  code simplified due to new parameter parsing and lots of other improvements in Moin code.
                  MiniPage functionality for the text parameter has been preserved.
    - 2008.01.25: [Moin 1.6] updated for Moin 1.6 by Dave Hein,
                  no functional changes.
    - 2006: [Moin 1.5] written by Clif Kussmaul
    - originally based on Color Macro
      Copyright (c) 2002 by Markus Gritsch <gritsch@iue.tuwien.ac.at>
"""

from MoinMoin import wikiutil
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser

"""
    Parameters that macro accepts are:
        - text (the text to be colored)
        - col  (optional text color)
        - bcol (optional background text color)
        - font (optional font)

    Examples:

    <<Color2(Hello World!,col=red,bcol=blue,font=18px courier)>>
    <<Color2(Hello World!,bcol=blue)>>
    <<Color2(Hello World!,orange)>>
"""

def macro_Color2(macro, text=None, col=None, bcol=None, font=None):
    f = macro.formatter

    if not text:
        return f.strong(1) + \
               f.text('Color2 examples : ') + \
               f.text('<<Color2(Hello World!,red,blue,18px courier)>>, ') + \
               f.text('<<Color2(Hello World!,col=red,bcol=blue,font=18px courier)>>, ') + \
               f.text('<<Color2(Hello World!,#8844AA)>>') + \
               f.strong(0) + f.linebreak(0)

    style = ''
    if col:
        style += 'color:%s; '            % col
    if bcol:
        style += 'background-color:%s; ' % bcol
    if font:
        style += 'font:%s; '             % font

    # Escape HTML stuff.
    text = wikiutil.escape(text)
    text = wikiutil.renderText(macro.request, WikiParser, text)
    text = text.strip()

    return f.rawHTML('<span style="%s">' % style) + text + f.rawHTML('</span>')
