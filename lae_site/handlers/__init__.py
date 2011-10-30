#! /usr/bin/env python

from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.util import Redirect, redirectTo
from twisted.web.resource import Resource

from lae_site.handlers.devpay_complete import DevPayPurchaseHandler, ActivationRequestHandler


def make_site(config):
    resource = File('content')

    resource.putChild('signup', Redirect( config.devpay_purchase_url ))
    resource.putChild('devpay-complete', DevPayPurchaseHandler())
    resource.putChild('activation-request', ActivationRequestHandler())

    return Site(resource, logPath="sitelogs")


class RedirectToHTTPS(Resource):
    """
    I redirect to the same path at https:.
    Thanks to rakslice at http://stackoverflow.com/questions/5311229/redirect-http-to-https-in-twisted
    """
    isLeaf = 0

    def render(self, request):
        newpath = request.URLPath()
        assert newpath.scheme != "https", "https->https redirection loop: %r" % (request,)
        newpath.scheme = "https"
        newpath.netloc = newpath.netloc.split(':')[0]  # strip port
        return redirectTo(newpath, request)

    def getChild(self, name, request):
        return self


def make_redirector_site():
    return Site(RedirectToHTTPS())
