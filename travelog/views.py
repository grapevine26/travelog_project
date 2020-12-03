import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse, HttpResponse
from django import VERSION as django_version
from django_summernote.views import SummernoteUploadAttachment
from django_summernote.forms import UploadForm
from django_summernote.utils import get_attachment_model, using_config, has_codemirror_config
from django.template.loader import render_to_string
from .forms import PostForm, SignupForm, LoginForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

if django_version >= (3, 0):
    from django.utils.translation import gettext as _
else:
    from django.utils.translation import ugettext as _
logger = logging.getLogger(__name__)


# Create your views here.
class Join(CreateView):
    template_name = 'travelog/join.html'
    form_class = SignupForm
    success_url = '/'


class Login(LoginView):
    template_name = 'travelog/login.html'
    authentication_form = LoginForm


class Main(TemplateView):
    template_name = 'travelog/main.html'


class WhoAreWe(TemplateView):
    template_name = 'travelog/who_are_we.html'


class Memories(ListView):
    template_name = 'travelog/memories.html'
    model = Post
    ordering = '-pk'
    paginate_by = 10


class MemoriesDetail(DetailView):
    template_name = 'travelog/memories_detail.html'
    model = Post


@method_decorator(login_required, name='dispatch')
class MemoriesWrite(CreateView):
    template_name = 'travelog/memories_write.html'
    form_class = PostForm
    success_url = '/memories'


@method_decorator(login_required, name='dispatch')
class MemoriesUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'travelog/memories_write.html'
    success_url = '/memories'

    # get object
    def get_object(self):
        review = get_object_or_404(Post, pk=self.kwargs['pk'])
        return review


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
