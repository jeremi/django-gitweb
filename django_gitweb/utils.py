import math
import pygments
import pygments.lexers as lexers
import pygments.formatters as formatters
from pygments.util import ClassNotFound
from django.utils.safestring import mark_safe

def human_filesize(bytes):
    bytes = int(bytes)
    if bytes is 0:
        return '0 bytes'
    log = math.floor(math.log(bytes, 1024))
    return "%0.2f %s" % (bytes / math.pow(1024, log), ['bytes', 'kb', 'mb', 'gb', 'tb'][int(log)])

def unescape_amp(text):
    return text.replace('&amp;', '&')

class NakedHtmlFormatter(formatters.HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)
    def _wrap_code(self, source):
        for i, t in source:
            yield i, t

def pygmentize(mime, blob):
    try:
        lexer = lexers.get_lexer_for_mimetype(mime)
    except ClassNotFound:
        try:
            lexer = lexers.get_lexer_by_name(mime)
        except:
            lexer = lexers.get_lexer_by_name('text')
        
    pygmented_string = pygments.highlight(blob, lexer, NakedHtmlFormatter())
    pygmented_string = unescape_amp(pygmented_string)
    
    return mark_safe(pygmented_string)
