from MoinMoin.wikiutil import get_unicode, get_bool, get_int, get_float

"""
    Copyright (C) 2010 Andy D'Arcy Jewell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
generates_headings = False

def macro_ImageZoom(macro,image_url,width=None,height=None,label=None):
    """ ImageZoom("image_url",width=None,height=None,label=None) - Displays an image thumbnail which when clicked opens full-size in a new window. """
    # arguments passed in can be None or a unicode 
    if label == None:
        label = "Click image to view full size."
    if width == None:
        width = ""
    else:
        width = """ width="%s" """ % str(width)
    if height == None:
        height = ""
    else:
        height = """ height="%s" """ % str(height)
    return u'''<img src="%s" %s %s onclick="window.open('%s')" ><br><small><em>%s</em></small>''' % (image_url, width, height, image_url, label)

