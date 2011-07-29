from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from feincms.module.page import processors
from feincms.module.page.models import Page
from feincms.views.base import Handler


class PreviewHandler(Handler):
    """
    Preview handler

    The methods used in this handler should not be considered official API.
    Everything here is subject to change.
    """

    def __call__(self, request, path, page_id):
        if not request.user.is_staff:
            return HttpResponseRedirect('/')

        page = get_object_or_404(Page, pk=page_id)

        # Throw out request processor which will cause the page to-be-previewed
        # to be seen as inactive (which is the case, of course)
        page.request_processors = [rp for rp in Page.request_processors if rp not in (
            processors.require_path_active_request_processor,)]

        # Remove _preview/42/ from URL, the rest of the handler code should not
        # know that anything about previewing. Handler.prepare will still raise
        # a 404 if the extra_path isn't consumed by any content type
        request.path = page.get_absolute_url()

        return self.build_response(request, page)
