from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from template_utils.markup import formatter

@staff_member_required
def format_preview(request): #called by markitup
    processed = ''
    if request.method == 'POST':
        processed = formatter(request.POST.get('data'))
    return HttpResponse(processed)
