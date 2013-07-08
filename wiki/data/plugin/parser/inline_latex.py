"""
inline_latex is a parser that allows regular moin moin wiki syntax,
but also latex style inline formulas like $...$ and latex style
paragraph formulas like $$...$$. Note that in the latter case, you
are (unlike in latex) limited to a single line. If you absolutely
need multiple lines, use the parser directly.

Copyright 2005 Johannes Berg <johannes@sipsolutions.net>
          2009 MoinMoin:ReimarBauer changed for 1.7.2/1.8 and the mathtran extension
Released under GPLv2.
"""
import re
from MoinMoin.parser import text_moin_wiki as wiki
from MoinMoin import wikiutil

class Parser(wiki.Parser):
    extensions = '*.tex'
    scan_rules = wiki.Parser.scan_rules
    scan_rules += ur'|(?P<latex_formula>\$[^$].*?(?<!\\)\$)'
    scan_rules += ur'|(?P<latex_formula_para>\$\$.*?(?<!\\)\$\$)'

    scan_re = re.compile(scan_rules, re.UNICODE|re.VERBOSE)

    def __init__(self, raw, request, **kw):
        wiki.Parser.__init__(self, raw, request, **kw)
        self.formatter = request.formatter
        self.request = request
        self.args = kw.get('format_args', '')
        self.mathtran_parser = wikiutil.importPlugin(self.request.cfg, 'parser', 'text_x_mathtran', 'Parser')

    def _latex_formula_repl(self, word, groups):
        word = word[1:len(word)-1]
        mp = self.mathtran_parser(word, self.request, format_args=self.args)
        if mp.init_settings:
            return mp.render(self.formatter)

    def _latex_formula_para_repl(self, word, groups):
        mp = self.mathtran_parser(word, self.request, format_args=self.args)
        if mp.init_settings:
            return "%s%s%s" % (self.formatter.paragraph(1), mp.render(self.formatter), self.formatter.paragraph(0))
