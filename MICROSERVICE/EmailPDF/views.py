from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from django.conf import settings
#from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from django.template.loader import get_template,render_to_string

#from firebase import firebase

class Send_email(APIView):
	def get(self,request,receiver,a,b):
		"""Editing Html"""
		template = get_template("index.html")
		template_vars = {"title": a,"national_pivot_table": b}
		html_out = template.render(template_vars)

		"""Generating PDF"""
		result = BytesIO()
		pdf = pisa.pisaDocument(BytesIO(html_out.encode("UTF-8")), result)
		if not pdf.err:
			try:
				# html to include in the body section
				body = """	Dear,
					
					This is my final report.
					
					Best Regards,	"""
				subject = "My Final ppt report"
				from_email = settings.EMAIL_HOST_USER
				to_list = [receiver]
				message = EmailMessage(subject, body, from_email, to_list)
				message.attach('report.pdf', result.getvalue(),'application/pdf')
				message.content_subtype = "html"
				message.send()
			except:
				return Response({'Error': 'Unable to send Email'}, status = HTTP_200_OK)
			"""try:
				firebase = firebase.FirebaseApplication('/PDF')
				client = storage.Client()
				bucket = client.get_bucket('microservice-e02eb.appspot.com')
				PDFBlob = bucket.blob('/')
				PDFBlob = bucket.blob("PDF/"+str(self.idNum)+"."+str(num))
				PDFBlob.upload_from_filename
				return Response({'Success': 'Email sent'}, status = HTTP_400_BAD_REQUEST)
			except:
			#send_mail(subject, message, from_email, to_list, fail_silently=True)"""
		else:
			return Response({'Error': 'Unable to generate PDF'}, status = HTTP_400_BAD_REQUEST)
