import base64
import datetime
import os
import random
import string

from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from smartalaba.settings import MEDIA_ROOT
from . import main

try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from datetime import date
from sendgrid import sendgrid, SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)

from smartalaba.settings import SENDGRID_API_KEY
from .models import Message, MessageImages, Transaction, Invoice
from .forms import ContactForm

# API security key:
# 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
#
# This is the admin section Not the Superadmin. Admin can:
#       1. view request(Messages) sent from the end user
#       2. Accept or reject the request via mails sent.
#       3. If accepted, admin can enter the money paid, made and the shipping cost and VAT then hit save.
#       4. Once saved, it is for records keeping and will goto the profits page where all Transactions are saved
#       5. If rejected, admin can view all in the rejected page and then review it later if it should be Accepted
#       6. Admin can create Feature products for any events going on. Can as well delete and start an event.
#       7. Once an event is created, status is false. If status is False it won't be seen in 'index'
#       8. The start/stop page has 2 dropdowns, 1 for the events created and the other to start/stop it.
#           if an event is started; staus = True therefore, shown in 'index' else status = False and taken out.
#       9. If an event is deleted...
#       10. admin can edit/delete an item in the feature product
#       11. anywhere you see 'pd' it means 'PageData' which is also 'context'
#

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

title = "SmartAlaba Ltd"
address = "30 Wetheral Road Owerri"
phone = "+234 808 568 0969"
email = "info@smartalaba.com"
site = "https://smartalaba.com/"
payment_details = "SmartAlaba Ltd"+"\n"+"Bank: FCMB"+"\n"+"Account holder: SmartAlaba Ltd"+"\n"+"Bank account: 6270292029"
payment_terms = "30 days"


# landing page for admin, 'admin-index' name: 'adminhome'
@login_required
def admin_home(request):
    num_req = Message.objects.all().count()  # number of total request
    num_wtn_req = Message.objects.filter(status="Waiting").count()  # number of waiting requests
    num_rej_req = Message.objects.filter(status="Rejected").count()  # number of rejected requests
    num_acp_req = Message.objects.filter(status="Accepted").count()  # number of accepted requests
    context = {
        'req': num_req,
        'wtn': num_wtn_req,
        'rej': num_rej_req,
        'acp': num_acp_req
    }
    return render(request, 'manageportal/admin-index.html', context=context)


@login_required
def message_list(request):
    msg_list = Message.objects.get_queryset().order_by('id')
    page = request.GET.get('page', 1)
    is_paginated = Paginator(msg_list, 5)

    try:
        messages = is_paginated.page(page)
    except PageNotAnInteger:
        messages = is_paginated.page(1)
    except EmptyPage:
        messages = is_paginated.page(is_paginated.num_pages)
    pd = {
        'msg': messages
    }
    return render(request, 'manageportal/message_list.html', context=pd)


@login_required
def message_detail(request, pk):
    msg = Message.objects.get(pk=pk)
    msg_image = MessageImages.objects.filter(message_id=msg.pk)
    photos = []
    upload = msg.uploaded_at
    for images in msg_image:
        img = images.image
        photos.append(img)

    pd = {
        'id': msg.id,
        'photo': photos,
        'uploaded_at': upload,
        'fullname': msg.fullname,
        'phone_number': msg.phone_number,
        'email': msg.email,
        'description': msg.description,
        'address': msg.address,
        'status': msg.status
    }
    return render(request, 'manageportal/message_detail.html', pd)

# rejected message detail page, 'reject_message.html', name: 'message-reject', url: message-rejected/message:ID
@login_required
def reject_message(request, id):
    msg = Message.objects.get(id=id)  # get a single message
    mail = msg.email
    context = {
        'my_name': msg.fullname,
        'my_mail': mail,
    }

    # if it's posted, change 'status' to "Rejected"
    if request.method == 'POST':
        msg.status = "Rejected"
        reply = request.POST.get("reply")
        message = Mail(
            from_email=("info@smartalaba.com", "Smartalaba"),
            to_emails=mail,
            subject='Request Rejected',
            html_content=reply
        )
        try:
            response = sg.send(message)
            print("Mail sent")
            print("===========Status code======\n", response.status_code)
            print("===========body=============\n", response.body)
            print("=============headers========\n", response.headers)
            msg.save()
        except Exception as e:
            print(e)
            return redirect('message-reject', id=id)

        return redirect('adminhome')
    return render(request, 'manageportal/reject_message.html', context)


# list of rejected messages, 'rejected_list.html', name: 'rejected-list', url: rejected-messages/
@login_required
def rejected_list(request):
    msg_list = Message.objects.filter(status="Rejected").order_by('-uploaded_at')  # get all where 'status="rejected"'
    page = request.GET.get('page', 1)
    is_paginated = Paginator(msg_list, 5)

    try:
        messages = is_paginated.page(page)
    except PageNotAnInteger:
        messages = is_paginated.page(1)
    except EmptyPage:
        messages = is_paginated.page(is_paginated.num_pages)
    pd = {
        'list': messages
    }
    return render(request, 'manageportal/rejected_list.html', pd)


# list of spammed messages, 'spam_list.html', name: 'spam-list', url: spam-messages/
@login_required
def spam_list(request):
    msg_list = Message.objects.filter(status="Spam").order_by('-uploaded_at')  # get all where 'status="spam"'
    page = request.GET.get('page', 1)
    is_paginated = Paginator(msg_list, 5)

    try:
        messages = is_paginated.page(page)
    except PageNotAnInteger:
        messages = is_paginated.page(1)
    except EmptyPage:
        messages = is_paginated.page(is_paginated.num_pages)
    pd = {
        'list': messages
    }
    return render(request, 'manageportal/spam_list.html', pd)


# mark a message as spam page, 'spam_mark.html', name: 'message-spam', url: message-spam/message:ID
@login_required
def mark_spam(request, id):
    msg = Message.objects.get(id=id)  # get a single message
    mail = msg.email
    context = {
        'fullname': msg.fullname,
        'mail': mail,
    }

    # if it's posted, change 'status' to "Spam"
    if request.method == 'POST':
        msg.status = "Spam"

        try:
            print("message saved")
            msg.save()
        except Exception as e:
            print(e)
            return redirect('message-spam')

        return redirect('adminhome')
    return render(request, 'manageportal/spam_mark.html', context)


# unmark a message as spam page, 'spam_unmark.html', name: 'message-unspam', url: message-unspam/message:ID
@login_required
def unmark_spam(request, id):
    msg = Message.objects.get(id=id)  # get a single message
    mail = msg.email
    context = {
        'fullname': msg.fullname,
        'mail': mail,
        'description': msg.description,
    }

    # if it's posted, change 'status' to "Spam"
    if request.method == 'POST':
        msg.status = "Waiting"

        try:
            print("message saved")
            msg.save()
        except Exception as e:
            print(e)
            return redirect('message-spam', id=id)

        return redirect('waiting-list')
    return render(request, 'manageportal/spam_unmark.html', context)


# delete spam message, 'spam_delete.html', name: 'message-delete', url: message-spam-delete/message:ID
@login_required
def delete_spam(request, id):
    msg = Message.objects.get(id=id)  # get a single message
    mail = msg.email
    context = {
        'fullname': msg.fullname,
        'mail': mail,
        'description': msg.description,
    }

    # if it's posted, change 'status' to "Spam"
    if request.method == 'POST':
        msg.delete()

        return redirect('messages')
    return render(request, 'manageportal/spam_delete.html', context)


# accept a message page, 'accept_a_message.html', name: 'message-accept', url: message-accept/message:ID
@login_required
def accept_a_message(request, id):
    msg = Message.objects.get(id=id)  # get a single message
    mail = msg.email
    context = {
        'fullname': msg.fullname,
        'mail': mail,
    }

    # if it's posted, change 'status' to "Accept"
    if request.method == 'POST':
        msg.status = "Accepted"

        try:
            print("message saved")
            msg.save()
        except Exception as e:
            print(e)
            return redirect('message-accept', id=id)

        return redirect('accepted-list')
    return render(request, 'manageportal/accept_a_message.html', context)


# accepted message detail page, 'accept_message.html', name: 'message-accept', url: message-accepted/message:ID
@login_required
def accept_message(request, id):
    msgObj = Message.objects.get(pk=id)  # get a single message
    # tnx = Transaction.objects.get(message_id=msgObj.pk)
    mail = msgObj.email
    user_address = msgObj.address
    description = msgObj.description
    user_name = msgObj.fullname
    dd = msgObj.uploaded_at
    send_date = str(dd.day) +"/"+ str(dd.month) +"/"+ str(dd.year)

    msg = ""
    css = ""

    # if it's posted, change 'status' to "Accepted"
    if request.method == 'POST':
        msgObj.status = "Accepted"
        reply = request.POST.get("reply")
        quantity = request.POST.get("qty")
        due_date = request.POST.get("due_date")
        discount = request.POST.get("discount")
        unit_price = request.POST.get("unit_price")
        total_price = int(unit_price) * int(quantity)
        net_total = total_price
        total_amount_due = 0.0
        discount = int(discount)
        if discount > 0:
            total_amount_due = net_total - (net_total * discount / 100)
        else:
            total_amount_due = net_total
        issue_date = date.today()
        pdf = main.PdfCreate()
        pdf.create_invoice_file(title, address, site, phone, email, user_name, user_address, description, discount,
                                send_date, quantity, unit_price, total_price, issue_date, due_date, net_total, total_amount_due, payment_details, payment_terms)

        file_name = user_name + '.pdf'

        # send mail
        email_body = reply+"<br>\n Please find Attachment to view Invoice"
        message = Mail(
            from_email=("info@smartalaba.com", "SmartAlaba"),
            to_emails=mail,
            subject='Request Accepted',
            html_content=email_body
        )

        file_path = 'docs/invoice/' + file_name
        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
        # Encode contents of file as Base 64
        encoded = base64.b64encode(data).decode()
        """Build attachment"""
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType("application/pdf")
        attachment.file_name = FileName("smartalaba_invoice.pdf")
        attachment.disposition = Disposition("attachment")
        attachment.content_id = ContentId("Invoice PDF ID")
        message.attachment = attachment
        try:
            response = sg.send(message)
            print("Mail sent")
            print("===========Status code======\n", response.status_code)
            print("===========body=============\n", response.body)
            print("=============headers========\n", response.headers)
            msg = 'Success'
            css = 'alert alert-success alert-dismissible fade show'
            data = Invoice.objects.create(message=msgObj, pdf_path=file_path)
            data.save()
        except Exception as e:
            msg = 'Failed'
            css = 'alert alert-danger alert-dismissible fade show'
            os.remove(file_path)
            print(e)
            return redirect('message-accepted', id=id)

    pd = {
        'my_name': user_name,
        'my_mail': mail,
        'my_address': user_address,
        'message': msg,
        'css': css
    }
    return render(request, 'manageportal/accept_message.html', pd)


# list of accepted messages, 'accepted_list.html', name: 'accepted-list', url: accepted-messages/
@login_required
def accepted_list(request):
    msg_list = Message.objects.filter(status="Accepted").order_by('-uploaded_at')  # get all where 'status="accepted"'
    done_list = []
    for child in msg_list:
        transaction_obj = Transaction.objects.filter(message_id=child.id).first()

        single_obj = {'obj': child}
        single_obj['ticks'] = "Not Done"
        single_obj['invoice'] = True

        if transaction_obj:
            single_obj['ticks'] = "Done"
        done_list.append(single_obj)
    page = request.GET.get('page', 1)
    is_paginated = Paginator(done_list, 5)

    try:
        messages = is_paginated.page(page)
    except PageNotAnInteger:
        messages = is_paginated.page(1)
    except EmptyPage:
        messages = is_paginated.page(is_paginated.num_pages)
    pd = {
        'list': messages,
    }
    return render(request, 'manageportal/accepted_list.html', pd)


# list of waiting messages, 'waiting_list.html', name: 'waiting-list', url: waiting-messages/
@login_required
def waiting_list(request):
    msg_list = Message.objects.filter(status="Waiting").order_by('-uploaded_at')  # get all where 'status="rejected"'
    pd = {
        'list': msg_list
    }
    return render(request, 'manageportal/waiting_list.html', pd)


@login_required
def profit_view(request):
    tnx_list = Transaction.objects.all()

    total_sales = Transaction.objects.values_list('money_paid', flat=True)
    tsales = sum(total_sales)

    total_income = Transaction.objects.values_list('money_made', flat=True)
    tcome = sum(total_income)

    print(tsales, tcome, "=======================")
    pd = {
        'tnx': tnx_list,
        'totalSales': tsales,
        'totalIncome': tcome
    }
    return render(request, 'manageportal/profit_page.html', pd)


@login_required
def search_view(request):
    query = request.GET.get('search-bar')
    option = request.GET.get('search-option')

    if option == 'uuid':
        if query is not None or query != '' or query != ' ':
            search_list = Transaction.objects.filter(uuid=query)
        else:
            return redirect('adminhome')
    else:
        if query is None or query == '' or query == ' ':

            return redirect('adminhome')
        else:
            search_list = Transaction.objects.filter(
                Q(uid__icontains=query) |
                Q(message__fullname__icontains=query) |
                Q(message__email__icontains=query)
            )

    pd = {
        'search': search_list
    }
    return render(request, 'manageportal/search_list.html', pd)


@login_required
def transaction_view(request, id):
    tnx = Message.objects.get(id=id)
    saved_tnx = Transaction.objects.filter(message_id=id)
    message = ""
    css = ""
    ptnx = None

    for stnx in saved_tnx:
        if stnx:
            ptnx = stnx
            message = 'Already done!'
            css = 'alert alert-primary alert-dismissible fade show'

    if request.method == 'POST':
        item_cost = float(request.POST['itemCost'])
        amount_paid = float(request.POST['amountPaid'])
        amount_made = float(request.POST['amountMade'])
        shipping_cost = float(request.POST['shippingCost'])
        vat = int(request.POST['vat'])
        uid = id_generator()

        print("============= Print ===============")
        print(amount_made, amount_paid, shipping_cost, vat)

        data = Transaction.objects.create(uid=uid, message=tnx, cost=item_cost, money_paid=amount_paid, money_made=amount_made,
                                          shipping_cost=shipping_cost, vat=vat)
        if data.save():
            message = 'Failed'
            css = 'alert alert-danger alert-dismissible fade show'
        else:
            message = 'Success'
            css = 'alert alert-success alert-dismissible fade show'
            tnx = None
    pd = {
        'tn': tnx,
        'tnxp': ptnx,
        'message': message,
        'css': css,
    }
    return render(request, 'manageportal/transaction_per_request.html', pd)


@login_required
def transaction_detail_view(request, pk):
    tnx = Transaction.objects.get(pk=pk)
    name = Message.objects.get(pk=tnx.message_id)
    msg_image = MessageImages.objects.filter(message_id=name.pk)
    photos = []
    for images in msg_image:
        img = images.image
        photos.append(img)
    mails = name.email
    cust_name = name.fullname
    cust_phone = name.phone_number
    item_photo = photos
    item_description = name.description

    context = {
        'id': tnx.uid,
        'name': cust_name,
        'phone': cust_phone,
        'mail': mails,
        'photo': item_photo,
        'des': item_description,
        'cost': tnx.cost,
        'moneyPaid': tnx.money_paid,
        'moneyMade': tnx.money_made,
        'shipping': tnx.shipping_cost,
        'vat': tnx.vat,
        'date': tnx.done_on
    }
    return render(request, 'manageportal/transaction_detail.html', context)


@login_required
def invoice_upload(request):
    message = ""
    if request.method == 'POST' and request.FILES['fileToUpload']:
        try:
            pdf = request.FILES['fileToUpload']
            store = 'docs/'+pdf.name
            fs = FileSystemStorage()
            fs.save(store, pdf)
            message = "File successfully saved!"
        except Exception as e:
            message = e
    pd = {
        'msg': message,
    }

    return render(request, 'manageportal/upload_file.html', pd)


# for the user to contact
def contact_view(request):
    my_form = ContactForm()
    context = {
        'message': '',
        'css': '',
        'form': my_form
    }

    if request.method == 'POST':
        my_form = ContactForm(request.POST, request.FILES)
        if my_form.is_valid():
            fullname = my_form.cleaned_data['fullname']
            phone = my_form.cleaned_data['phone_number']
            email = my_form.cleaned_data['email']
            address = my_form.cleaned_data['address']
            description = my_form.cleaned_data['description']
            image = my_form.cleaned_data['image_uploads']

            print("Before saving...")
            print(fullname, phone, email, address, description)

            data = Message(fullname=fullname, phone_number=phone, address=address, email=email,
                           description=description, image=image)

            # if data.clean():
            if data.save():
                print("Saving...")
                print(fullname, phone, email, address, description)
                ContactForm()
                context = {
                    'message': 'Failed to send',
                    'css': 'text-align:center; background-color:red;'
                }
            else:
                ContactForm()
                context = {
                    'message': 'Successfully sent',
                    'css': 'text-align:center; background-color:green;'
                }
        else:
            ContactForm()
            context = {
                'message': 'Error sending message',
                'css': 'text-align:center; background-color:red;'
            }
    else:
        ContactForm()

    print("After saving...")
    return render(request, 'manageportal/contact.html', context)


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    unique_codes = ''.join(random.choice(chars) for _ in range(size))
    return unique_codes


# ================================================================================================
#                   codes to be used later mayber
# class MessageListView(LoginRequiredMixin, generic.ListView):
#     model = Message
#     paginate_by = 10
#
#
# class MessageDetailView(LoginRequiredMixin, generic.DetailView):
#     model = Message
# @login_required
# def invoice_view(request):
#     tnx_list = Transaction.objects.all()
#     pd = {
#         'tnx': tnx_list,
#     }
#     return render(request, 'manageportal/invoice.html', pd)
#
#
# @login_required
# def create_invoice_view(request, pk):
#     tnx = Transaction.objects.get(pk=pk)
#     name = Message.objects.get(pk=tnx.message_id)
#     mails = name.email
#     cust_name = name.fullname
#     cust_phone = name.phone_number
#     item_photo = name.image
#     item_name = name.product_name
#     item_description = name.description
#     cost = tnx.cost
#     profit = tnx.money_made
#     paid = tnx.money_paid
#     shipping = tnx.shipping_cost
#     vat = tnx.vat
#     uuid = tnx.uuid
#
#     msg = ""
#     css = ""
#
#     if request.method == 'POST':
#         # reply = request.POST.get("reply")
#         due_date = request.POST.get("ddate")
#         sent_date = datetime.date.today()
#
#         pdf = main.PdfCreate()
#         pdf.create_invoice_file(cust_name, sent_date, due_date, mails, customer_care, profit, shipping, item_name,
#                                 vat, uuid, cost, sub_title="Invoice for")
#
#         file_name = cust_name + '_' + str(sent_date) + '.pdf'
#
#         # send mail
#         email_body = "Please find Attachment to view Invoice"
#         message = Mail(
#             from_email=("info@smartalaba.com", "Smartalaba"),
#             to_emails=mails,
#             subject='Invoice',
#             html_content=email_body
#         )
#         file_path = 'docs/invoice/' + file_name
#         with open(file_path, 'rb') as f:
#             data = f.read()
#             f.close()
#
#         # Encode contents of file as Base 64
#         encoded = base64.b64encode(data).decode()
#
#         """Build attachment"""
#         attachment = Attachment()
#         attachment.file_content = FileContent(encoded)
#         attachment.file_type = FileType("application/pdf")
#         attachment.file_name = FileName("smartalaba_invoice.pdf")
#         attachment.disposition = Disposition("attachment")
#         attachment.content_id = ContentId("Invoice PDF ID")
#         message.attachment = attachment
#         try:
#             response = sg.send(message)
#             print("===========Status code======\n", response.status_code)
#             print("===========body=============\n", response.body)
#             print("=============headers========\n", response.headers)
#             msg = 'Success'
#             css = 'alert alert-success alert-dismissible fade show'
#             data = Invoice.objects.create(message=name, pdf_path=file_path)
#             data.save()
#         except Exception as e:
#             msg = 'Failed'
#             css = 'alert alert-danger alert-dismissible fade show'
#             os.remove(file_path)
#             print(e)
#
#     context = {
#         'id': uuid,
#         'name': cust_name,
#         'phone': cust_phone,
#         'mail': mails,
#         'photo': item_photo,
#         'des': item_description,
#         'cost': cost,
#         'moneyPaid': paid,
#         'moneyMade': profit,
#         'shipping': shipping,
#         'vat': vat,
#         'date': tnx.done_on,
#         'message': msg,
#         'css': css,
#     }
#     return render(request, 'manageportal/create_invoice.html', context)
#
#
# @login_required
# def receipt_view(request):
#     tnx_list = Transaction.objects.all()
#     pd = {
#         'tnx': tnx_list,
#     }
#     return render(request, 'manageportal/receipt.html', pd)
#
#
# @login_required
# def create_receipt_view(request, pk):
#     tnx = Transaction.objects.get(pk=pk)
#     name = Message.objects.get(pk=tnx.message_id)
#     mails = name.email
#     cust_name = name.fullname
#     item_name = name.product_name
#     item_description = name.description
#     cost = tnx.cost
#     money_paid = tnx.money_paid
#     shipping = tnx.shipping_cost
#     uuid = tnx.uuid
#
#     msg = ""
#     css = ""
#
#     # send pdf
#     if request.method == 'POST':
#         balance = request.POST.get("balance")
#         sent_date = datetime.date.today()
#         pdf = main.PdfCreate()
#         pdf.create_receipt_file(cust_name, sent_date, mails, customer_care, money_paid, shipping, item_name,
#                                 uuid, cost, balance, sub_title="Receipt for")
#         file_name = cust_name + '_' + str(sent_date) + '.pdf'
#
#         # send mail
#         email_body = "Please find Attachment to view Receipt"
#         mail = Mail(
#             from_email=("info@smartalaba.com", "Smartalaba"),
#             to_emails=mails,
#             subject='Receipt',
#             html_content=email_body
#         )
#         file_path = 'docs/receipt/' + file_name
#         with open(file_path, 'rb') as f:
#             data = f.read()
#             f.close()
#
#         # Encode contents of file as Base 64
#         encoded = base64.b64encode(data).decode()
#
#         """Build attachment"""
#         attachment = Attachment()
#         attachment.file_content = FileContent(encoded)
#         attachment.fiel_type = FileType("application/pdf")
#         attachment.file_name = FileName("smartalaba_receipt.pdf")
#         attachment.disposition = Disposition("attachment")
#         attachment.content_id = ContentId("Receipt PDF ID")
#         mail.attachment = attachment
#         try:
#             # response = sg.send(mail)
#             # print("Mail sent")
#             # print("===========Status code======\n", response.status_code)
#             # print("===========body=============\n", response.body)
#             # print("=============headers========\n", response.headers)
#             msg = 'Success'
#             css = 'alert alert-success alert-dismissible fade show'
#             data = Receipt.objects.create(message=name, pdf_path=file_path)
#             # data.save()
#         except Exception as e:
#             msg = 'Failed'
#             css = 'alert alert-danger alert-dismissible fade show'
#             os.remove(file_path)
#             print(e)
#
#     bal = float(cost) - float(money_paid)
#     print("=========", msg, "===========", css)
#     pd = {
#         'id': uuid,
#         'name': cust_name,
#         'item_name': item_name,
#         'balance': bal,
#         'mail': mails,
#         'des': item_description,
#         'cost': cost,
#         'moneyPaid': money_paid,
#         'shipping': shipping,
#         'date': tnx.done_on,
#         'message': msg,
#         'css': css,
#     }
#     return render(request, 'manageportal/create_receipt.html', pd)
#
#
# @login_required
# def feature_view(request):
#     ftr_list = FeatureProducts.objects.all()
#     pd = {
#         'feat': ftr_list
#     }
#     return render(request, 'manageportal/feature_page.html', pd)
#
#
# @login_required
# def feature_view_create(request):
#     pd = {
#         'message': '',
#         'css': ''
#     }
#     if request.method == 'POST':
#         event_name = request.POST['eventName']
#         name = request.POST['name']
#         price = float(request.POST['price'])
#         shipping_cost = float(request.POST['shippingCost'])
#         vat = float(request.POST['vat'])
#         photo = request.FILES['photo']
#         details = request.POST['details']
#         quantity = request.POST['quantity']
#         start_date = request.POST['startdate']
#         end_date = request.POST['endate']
#         # start_date = datetime.datetime.now()
#         # today = datetime.date.today()
#         # end_date = today + datetime.timedelta(days=1)
#
#         data = FeatureProducts(event_name=event_name, name=name, price=price, photo=photo, shipping_cost=shipping_cost,
#                                vat=vat, details=details, quantity_in_stock=quantity, start_date=start_date,
#                                end_date=end_date)
#         if data.save():
#             pd = {
#                 'message': 'Failed',
#                 'css': 'bg-red tc'
#             }
#         else:
#             pd = {
#                 'message': 'Success',
#                 'css': 'bg-green tc'
#             }
#     return render(request, 'manageportal/feature_create.html', pd)
#
#
# @login_required
# def feature_view_save(request):
#     pd = {}
#     if request.method == 'GET':
#         feat = FeatureProducts.objects.values('event_name').distinct()
#         feat.query.group_by = ['event_name']
#
#         pd = {
#             'message': '',
#             'css': '',
#             'feat_list': feat
#         }
#
#     if request.method == 'POST':
#         status_option = request.POST.get('status')
#         events = request.POST.get('events')
#         feat_list = FeatureProducts.objects.filter(event_name=events)
#         if status_option == "start":
#             feat_list.update(status=True)
#         elif status_option == "stop":
#             feat_list.update(status=False)
#         else:
#             feat_list.update(status=False)
#
#         return redirect('features')
#
#     return render(request, 'manageportal/feature_save.html', pd)
#
#
# def coupons_view(request):
#     status = True
#     pd = {}
#     products = FeatureProducts.objects.filter(status=status)
#     if request.method == 'GET':
#         pd = {
#             'uuid': id_generator(),
#             'product': products
#         }
#
#     if request.method == 'POST':
#         p = products[0].pk
#         pro = FeatureProducts.objects.get(id=p)
#         code = request.POST['code']
#         name = request.POST.get('product_name')
#         discount = request.POST['discount']
#         product_quantity_used = request.POST['number_of_products']
#         start_date = products[0].start_date
#         end_date = products[0].end_date
#
#         data = Coupons(code=code, product=pro, discount=discount, product_quantity_used=product_quantity_used,
#                        start_date=start_date, end_date=end_date)
#         if products[0].name == name:
#             data.save()
#             return redirect('coupons')
#             # print("===============Success==================")
#         else:
#             print("==============Error occurred! ================")
#             pd
#
#     return render(request, 'manageportal/coupon.html', pd)
#
