from django.urls import path
from EmailPDF.views import Send_email

urlpatterns = [
	path('email/<receiver>/<a>/<b>',Send_email.as_view()),
]