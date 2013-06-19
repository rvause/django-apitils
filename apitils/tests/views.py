from django.views.generic import View

from apitils.views import NoCSRFMixin, JSONResponseMixin, JSONPayloadMixin


class APIView(JSONResponseMixin, NoCSRFMixin, JSONPayloadMixin, View):
    def get(self, request):
        return self.render({'success': True})

    def post(self, request):
        return self.render(request.POST)

    def put(self, request):
        return self.render(request.payload)
