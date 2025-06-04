from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
#CBV styleeeee
class HybridRenderView(APIView):
    template_name = None  # override in subclass

    def render_response(self, request, context):
        if settings.SERVER_SIDE_RENDERING and self.template_name:
            return render(request, self.template_name, context)
        return JsonResponse(context)
'''

from core.shared.HybridRenderView import HybridRenderView

class MyView(HybridRenderView):
    template_name = 'my_template.html'

    def get(self, request, *args, **kwargs):
        data = {
            "foo": "bar",
            "list": [1, 2, 3]
        }
        return self.render_response(request, data)

'''


#FBV styleeee
def hybrid_response(request, template_name, context):
    if settings.SERVER_SIDE_RENDERING:
        return render(request, template_name, context)
    return JsonResponse(context)

'''
def my_view(request):
    data = {...}
    return hybrid_response(request, 'my_template.html', data)


'''