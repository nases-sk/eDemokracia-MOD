import cgi

from paste.urlparser import PkgResourcesParser
from pylons import request, tmpl_context as c
from pylons.controllers.util import forward
from webhelpers.html.builder import literal
import logging
import urllib
from ckan.lib.base import BaseController
from ckan.lib.base import render
import ckan.lib.base as base


class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    def document(self):
        """Render the error document"""
        original_request = request.environ.get('pylons.original_request')        
        if (original_request.referer != None) and (('%22'  in original_request.referer) or ('%3C' in original_request.referer) or ('(' in original_request.referer)) and ('fanstatic' in original_request.referer):
            base.abort(400)
            #return base.redirect(controller="home", action="index")
        if (original_request.path != None) and (('%22'  in original_request.path) or ('%3C' in original_request.path) or ('(' in original_request.path)) and ('fanstatic' in original_request.path):
            base.abort(400)
            #return base.redirect(controller="home", action="index")
        
        #original_request = urllib.urlencode(original_request)
        original_response = request.environ.get('pylons.original_response')
        # When a request (e.g. from a web-bot) is direct, not a redirect
        # from a page. #1176
        if not original_response:
            return 'There is no error.'
        # Bypass error template for API operations.
        if original_request and original_request.path.startswith('/api'):
            return original_response.body
        # Otherwise, decorate original response with error template.
        c.content = literal(original_response.unicode_body) or \
            cgi.escape(request.GET.get('message', ''))
        c.prefix = request.environ.get('SCRIPT_NAME', ''),
        c.code = cgi.escape(request.GET.get('code',
                            str(original_response.status_int))),
        return render('error_document_template.html')

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file('/'.join(['media/img', id]))

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file('/'.join(['media/style', id]))

    def _serve_file(self, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        request.environ['PATH_INFO'] = '/%s' % path
        return forward(PkgResourcesParser('pylons', 'pylons'))
