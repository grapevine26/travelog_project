import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, UpdateView, FormView, CreateView
from django.http import JsonResponse, HttpResponse
from .forms import PostForm
from django import VERSION as django_version
from django_summernote.views import SummernoteUploadAttachment
from django_summernote.forms import UploadForm
from django_summernote.utils import get_attachment_model, using_config, has_codemirror_config
from django.template.loader import render_to_string
if django_version >= (3, 0):
    from django.utils.translation import gettext as _
else:
    from django.utils.translation import ugettext as _
logger = logging.getLogger(__name__)


# Create your views here.
class Join(TemplateView):
    template_name = 'travelog/join.html'


class Login(TemplateView):
    template_name = 'travelog/login.html'


class Main(TemplateView):
    template_name = 'travelog/main.html'


class WhoAreWe(TemplateView):
    template_name = 'travelog/who_are_we.html'


class Memories(TemplateView):
    template_name = 'travelog/memories.html'


class MemoriesDetail(TemplateView):
    template_name = 'travelog/memories_detail.html'


class MemoriesWrite(CreateView):
    template_name = 'travelog/memories_write.html'
    form_class = PostForm
    success_url = '/memories'


class FootPrints(TemplateView):
    template_name = 'travelog/footprints.html'


class Tips(TemplateView):
    template_name = 'travelog/tips.html'


class Contact(TemplateView):
    template_name = 'travelog/contact.html'


class SummernoteUpload(SummernoteUploadAttachment):
    @using_config
    def post(self, request, *args, **kwargs):
        print(request.user)
        print(request.FILES)
        print(request.POST)

        if not request.FILES.getlist('files'):
            return JsonResponse({
                'status': 'false',
                'message': _('No files were requested'),
            }, status=400)

        # remove unnecessary CSRF token, if found
        kwargs = request.POST.copy()
        kwargs.pop('csrfmiddlewaretoken', None)

        for file in request.FILES.getlist('files'):
            form = UploadForm(
                files={
                    'file': file,
                }
            )
            if not form.is_valid():
                logger.error(
                    'User<%s:%s> tried to upload non-image file.',
                    getattr(request.user, 'pk', None),
                    request.user
                )

                return JsonResponse(
                    {
                        'status': 'false',
                        'message': ''.join(form.errors['file']),
                    },
                    status=400
                )

        try:
            attachments = []

            for file in request.FILES.getlist('files'):

                # create instance of appropriate attachment class
                klass = get_attachment_model()
                attachment = klass()
                attachment.file = file

                # calling save method with attachment parameters as kwargs
                attachment.save(**kwargs)

                # choose relative/absolute url by config
                attachment.url = attachment.file.url

                attachments.append(attachment)

            return HttpResponse(render_to_string('django_summernote/upload_attachment.json', {
                'attachments': attachments,
            }), content_type='application/json')
        except IOError:
            return JsonResponse({
                'status': 'false',
                'message': _('Failed to save attachment'),
            }, status=500)
