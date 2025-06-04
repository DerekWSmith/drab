'''

The following is  UNtested example views for handling file uploads.
Use it to learn from and base the real view from.


'''

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from core.models import Item, ItemAttachment
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views import View

from core.shared.HybridRenderView import HybridRenderView

class ItemAttachmentUploadView(CreateView):
    model = ItemAttachment
    fields = ['file', 'filename']
    template_name = 'upload.html'
    success_url = reverse_lazy('item_list')  # adjust as needed

    def form_valid(self, form):
        item_id = self.kwargs.get('item_id')
        item = Item.objects.get(id=item_id)

        form.instance.content_type = ContentType.objects.get_for_model(Item)
        form.instance.object_id = item.id
        form.instance.uploaded_by = self.request.user
        form.instance.filename = form.cleaned_data['file'].name
        form.instance.attached_to = item  # optional, for clarity

        return super().form_valid(form)



class ItemAttachmentUploadView(View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        file = request.FILES.get('file')
        if not item_id or not file:
            return JsonResponse({'error': 'Missing item_id or file'}, status=400)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

        attachment = ItemAttachment(
            content_type=ContentType.objects.get_for_model(Item),
            object_id=item.id,
            file=file,
            filename=file.name,
            uploaded_by=request.user
        )
        attachment.save()

        return JsonResponse({'status': 'success', 'attachment_id': attachment.id})


class DRFview(HybridRenderView):
    template_name = 'my_template.html'

    def get(self, request, *args, **kwargs):
        data = {"foo": "bar", "list": [1, 2, 3]}
        return self.render_response(request, data)