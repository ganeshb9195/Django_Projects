import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import get_connection, EmailMessage
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def Email_Sending(request):
    if request.method == 'POST':
        try:
            with get_connection(
                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                recipient_list = request.POST.get("email").split()
                subject = request.POST.get("subject")
                email_from = settings.EMAIL_HOST_USER
                message = request.POST.get("message")
                attachment = request.FILES.get("attachment")
                if attachment:
                    fs = FileSystemStorage()
                    attachment_name = fs.save(attachment.name, attachment)
                    attachment_path = os.path.join(settings.MEDIA_ROOT, attachment_name)
                    print("Attachment Path:", attachment_path)
                msg = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
                if attachment:
                    msg.attach_file(attachment_path)
                msg.send()
                # Display success message
            messages.success(request,"Email Send Successfully...!")
        except Exception as e:
            # Display error message
            messages.error(request, f'Error sending email: {str(e)}')

    return render(request, 'Home.html')
