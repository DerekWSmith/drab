from django.utils import timezone



def upload_to(instance, filename):
    ts = timezone.now().strftime('%Y%m%d%H%M%S')
    model = instance.content_type.model
    return f'{instance.uploaded_by.id}/attachments/{model}/{instance.object_id}/{ts}_{filename}'