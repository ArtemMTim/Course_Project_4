from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Recipient, Message, Mailing, Mailing_Attempts

class MailingView(TemplateView):
    models = [Recipient, Mailing]
    template_name = 'mailing/main.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients_all'] = Recipient.objects.all()
        context['mailing_all'] = Message.objects.all()
        context['mailing_active'] = Mailing.objects.filter(status=Mailing.ACTIVE)
        return context

class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'

class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'

class RecipientCreateView(CreateView):
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')
    def get_success_url(self):
        return reverse_lazy('mailing:recipient_detail', kwargs={'pk': self.object.pk})

class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')

class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'

class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'

class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'text']
    template_name ='mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'text']
    template_name ='mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')
    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})

class MessageDeleteView(DeleteView):
    model = Message
    template_name ='mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

class MailingListView(ListView):
    model = Mailing
    template_name ='mailing/mailing_list.html'

class MailingDetailView(DetailView):
    model = Mailing
    template_name ='mailing/mailing_detail.html'

class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_at', 'end_at','status','message','recipients']
    template_name ='mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_at', 'end_at','status','message','recipients']
    template_name ='mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')
    def get_success_url(self):
        return reverse_lazy('mailing:mailing_detail', kwargs={'pk': self.object.pk})

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name ='mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

