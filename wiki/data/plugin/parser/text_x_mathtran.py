# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - mathtran

    This parser is used to visualize latex formulars using a mathtran server, e.g.
    http://www.mathtran.org

    Many thanks to Jonathan Fine for our discussions at the EuroPython Conference during
    the MoinMoin sprint session in Vilnius

    Please honor this work by adding a credits entry to the mathtran project on your wiki.
    "<a href="http://www.mathtran.org/" title="MoinMoin uses the Mathtran Online translation of mathematical content software.">MathTran Powered</a>"

    @copyright: 2008-2009 by MoinMoin:ReimarBauer
    @license: GNU GPL, see COPYING for details.
"""
import urllib
from MoinMoin import caching, config, wikiutil
from MoinMoin.action import AttachFile, cache

try:
    import urllib
except ImportError:
    urllib = None

def mathtran_settings(formular=u'', scale_factor=(u"3", u"1", u"2", u"4", u"5"),
                      mathtran_server=u"http://www.mathtran.org/cgi-bin/toy/"):
    """ dummy function to initialize all default parameters for mathtran. The parameters are checked for wrong input.
    @param formular: latex formular
    @param scale_factor: scale factor for result image of latex formular
    """
    return locals()

Dependencies = ["page"]

class Parser:
    """ mathtran parser """
    extensions = '*.tex'
    def __init__(self, raw, request, **kw):
        self.pagename = request.page.page_name
        self.raw = raw.strip('\n')
        self.request = request
        self.formatter = request.formatter
        self.form = None
        self._ = request.getText

        args = kw.get('format_args', '')
        self.init_settings = False
        try:
            settings = wikiutil.invoke_extension_function(request, mathtran_settings, args)
            for key, value in settings.items():
                setattr(self, key, value)
            # saves the state of valid input
            self.init_settings = True
        except ValueError, err:
            msg = u"mathtran: %s" % err.args[0]
            request.write(self.formatter.text(msg))

    def render(self, formatter):
        """ renders formular  """

        _ = self._

        # checks if initializing of all attributes in __init__ was done
        if not self.init_settings:
            return

        text = """%(mathtran_server)s?;D=%(scale_factor)s;tex=%(formular)s""" % {
                                                                                 "mathtran_server": self.mathtran_server,
                                                                                 "formular": wikiutil.url_quote(self.raw),
                                                                                 "scale_factor": self.scale_factor,
                                                                                }
        key = cache.key(self.request, itemname=self.pagename, content=text)
        if not cache.exists(self.request, key) and urllib:
            # ToDo add a timeout
            image = urllib.urlopen(text)
            cache.put(self.request, key, image.read(),
                      content_type="image/png")
        if cache.exists(self.request, key):
            credits = """<a href="http://www.mathtran.org/" title="MoinMoin uses the Mathtran Online translation of mathematical content software.">MathTran Powered</a>"""
            if not credits in self.request.cfg.page_credits:
                self.request.cfg.page_credits.append(credits)
                # ToDo show the credits only on pages using the parser extension
        return formatter.image(src=cache.url(self.request, key), alt=self.raw)

    def format(self, formatter):
        """ parser output """
        # checks if initializing of all attributes in __init__ was done
        if self.init_settings:
            self.request.write(self.formatter.div(1, css_class="mathtran"))
            self.request.write(self.render(formatter))
            self.request.write(self.formatter.div(0))

