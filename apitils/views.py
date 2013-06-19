import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


class NoCSRFMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *ar, **kw):
        return super(NoCSRFMixin, self).dispatch(*ar, **kw)


class JSONResponseMixin(object):
    def render(self, context):
        return HttpResponse(json.dumps(context), 'application/json')


class JSONPayloadMixin(object):
    def dispatch(self, request, *ar, **kw):
        try:
            request.payload = json.loads(request.body)
        except ValueError:
            request.payload = None
        return super(JSONPayloadMixin, self).dispatch(request, *ar, **kw)
