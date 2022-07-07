from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import os

def send_an_email(subject='' , message='', recipient_list='', attachment=''):
    if attachment:
        email = EmailMessage(subject, message, to=recipient_list, from_email=settings.EMAIL_HOST_USER)
        email.attach_file(attachment)
        email.send()
        return True
    else:
        email = EmailMessage(subject, message, to=recipient_list, from_email=settings.EMAIL_HOST_USER)
        email.send()
        return True
    return True


def send_mail(to, template, context):
    html_content = render_to_string(f'appointments/emails/{template}.html', context)
    text_content = "You have successfully paid fees , you can check details below."
    msg = EmailMultiAlternatives(context['subject'], text_content, settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("HTML Email Sent")



def send_an_email_with_html(request, email, object):
    context = {
        'subject': _('Congratulations !!! You have successfully paid the fees'),
        'appointment': object
        # 'uri': request.build_absolute_uri(reverse('accounts:activate', kwargs={'code': code})),
    }

    send_mail(email, 'paid_invoice', context)
#
# try:
#     subject = 'Your Data to AWS is Syncd Successfully'
#     message = 'You have successfully syncd data to AWS Cloud . Which means your data is safe'
#     recipient_list = ['abhishek.budruk@gmail.com', ]
#     attachment = os.path.join(settings.BASE_DIR, 'edb.pdf')
#     send_an_email(subject=subject, message=message, recipient_list=recipient_list, attachment=attachment)
# except Exception as e:
#     print(e)
#     print("Could not Sent an Email")
#     pass