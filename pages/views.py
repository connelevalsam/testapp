from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render

from manageportal.models import Message, MessageImages

from manageportal.forms import ContactForm, ContactUsForm


def home_view(request):
    my_form = ContactForm()
    context = {
        'message': '',
        'css': '',
        'form': my_form,
    }

    if request.method == 'POST':
        my_form = ContactForm(request.POST, request.FILES)
        if my_form.is_valid():
            fullname = my_form.cleaned_data['fullname']
            p_name = my_form.cleaned_data['product_name']
            phone = my_form.cleaned_data['phone_number']
            email = my_form.cleaned_data['email']
            address = my_form.cleaned_data['address']
            description = my_form.cleaned_data['description']

            data = Message.objects.create(fullname=fullname, product_name=p_name, phone_number=phone, address=address, email=email, description=description)

            for file in request.FILES.getlist('images'):
                instance = MessageImages(
                    message_id=data.pk,
                    image=file
                )
                instance.save()

            # if data.clean():
            if data.save():
                ContactForm()
                context = {
                    'message': 'Failed to send',
                    'css': 'text-align:center; background-color:red;',
                    'form': my_form
                }
            else:
                m = '''Dear Customer,
                Thank you for your enquiry, 
                we will be in touch within the next 24 hours
                
                Yours sincerely,\n\n

                SmartAlaba Team'''
                my_form = ContactForm()
                context = {
                    'message': m,
                    'css': 'display: inline-block; width: 80%; text-align:left; background-color:white; margin: auto;',
                    'form': my_form
                }
        else:
            ContactForm()
            context = {
                'message': 'Error sending message, check required fields',
                'css': 'text-align:center; background-color:red;',
                'form': my_form
            }
    return render(request, 'index.html', context)


def reach_us_view(request):
    my_form = ContactUsForm()
    context = {
        'message': '',
        'flag': '',
        'css': '',
        'form': my_form
    }

    if request.method == 'POST':
        my_form = ContactUsForm(request.POST)
        if my_form.is_valid():
            fullname = my_form.cleaned_data['fullname']
            phone = my_form.cleaned_data['phone_number']
            email = my_form.cleaned_data['email']
            message = my_form.cleaned_data['message']

            fullname = " " + fullname

            smartalaba_mail = 'info@smartalaba.com'
            if phone is None:
                phone = "No phone Number"
            elif fullname is None and email is None and message is None:
                context = {
                    'message': 'Important fields should be filled',
                    'flag': 'Failed',
                    'css': 'alert alert-danger alert-dismissible fade show',
                    'form': my_form
                }
            else:
                full_message = "Full name: " + str(fullname) + "<br>" + "Phone: " + str(phone) + "<br>" \
                               + "E-mail: " + str(email) + "<br>" + "Message: " + str(message)
                # send_mail('Contact', full_message, (email, fullname), [smartalaba_mail], fail_silently=True)
                send_msg = EmailMessage(
                    'Contact',
                    full_message,
                    (email, fullname),
                    [smartalaba_mail]
                )
                send_msg.content_subtype = "html"
                send_msg.send()
                context = {
                    'message': 'Sending mail',
                    'flag': 'Success',
                    'css': 'alert alert-success alert-dismissible fade show',
                    'form': my_form
                }
            print("=============================", fullname, phone, email, message)
        else:
            context = {
                'message': 'Invalid fields',
                'flag': 'Error sending mail. ',
                'css': 'alert alert-warning alert-dismissible fade show',
                'form': my_form
            }
    return render(request, 'reach-us.html', context)


# def test_view(request):
#     src = FeatureProducts.objects.filter(status=True)
#     pd = {
#         'photos': src
#     }
#     return render(request, 'test.htm', pd)
#
#
# def product_list_view(request):
#     p = FeatureProducts.objects.filter(status=True)
#
#     pd = {
#         'products': p
#     }
#     return render(request, 'feature_product_list.html', pd)
#
#
# def product_detail_view(request, id):
#     product = FeatureProducts.objects.get(id=id)
#     coupons = Coupons.objects.get(product_id=id)
#     main_price = product.price
#     discount = coupons.discount
#     new_price = (main_price * discount) / 100
#     new_price = main_price - new_price
#     prices = "N" + str(new_price) + "  N" + str(main_price)
#
#     print("Values=========", main_price, discount, new_price, prices)
#
#     pd = {
#         'eventName': product.event_name,
#         'product': product.name,
#         'price': prices,
#         'image': product.photo,
#         'shipping': product.shipping_cost,
#         'details': product.details,
#         'quantity': product.quantity_in_stock,
#         'begin': product.start_date,
#         'end': product.end_date
#     }
#     return render(request, 'feature_product_list_detail.html', pd)
