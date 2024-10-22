from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

class MailingView(TemplateView):
    template_name = 'mailing/mailing_list.html'