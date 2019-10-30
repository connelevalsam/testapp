from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='adminhome'),
    path('messages/', views.message_list, name='messages'),
    path('message/<int:pk>', views.message_detail, name='message-detail'),

    path('profits/', views.profit_view, name='profits'),
    path('profit-list/<int:pk>', views.transaction_detail_view, name='transaction-detail'),
    path('transaction-of/<int:id>/', views.transaction_view, name='transaction'),


    path('message-rejected/<int:id>', views.reject_message, name='message-reject'),
    path('message-accept/<int:id>', views.accept_a_message, name='message-accept'),
    path('message-accepted/<int:id>', views.accept_message, name='message-accepted'),

    path('waiting-messages/', views.waiting_list, name='waiting-list'),
    path('rejected-messages/', views.rejected_list, name='rejected-list'),
    path('accepted-messages/', views.accepted_list, name='accepted-list'),

    path('spam-messages/', views.spam_list, name='spam-list'),
    path('message-spam/<int:id>', views.mark_spam, name='message-spam'),
    path('message-unspam/<int:id>', views.unmark_spam, name='message-unspam'),
    path('message-delete-spam/<int:id>', views.delete_spam, name='message-delete'),

    path('upload-invoice/', views.invoice_upload, name='invoice-upload'),
    path('search/', views.search_view, name='search'),


    # path('features/', views.feature_view, name='features'),
    # path('features/create/', views.feature_view_create, name='feature_create'),
    # path('features/save/', views.feature_view_save, name='feature_save'),
    # path('coupons/', views.coupons_view, name='coupons'),
    # path('receipt/', views.receipt_view, name='receipt'),
    # path('send-receipt/<int:pk>', views.create_receipt_view, name='send_receipt'),
    # path('invoice/', views.invoice_view, name='invoice'),
    # path('send-invoice/<int:pk>', views.create_invoice_view, name='send_invoice'),
    # path('msgs/', views.MessageListView.as_view(), name='msgs'),
    # path('msgs-list/<int:pk>', views.MessageDetailView.as_view(), name='msg-detail'),
]
