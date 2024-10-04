from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET': # retrieve all products from the database
        product = Product.objects.all() # Fetch all products from the database
        serialiser = ProductSerializer(product, many=True) # Serialize the product data
        return Response(serialiser.data)  # Return the serialized data as a JSON response
    
    if request.method == 'POST': # create a new product
        serialiser = ProductSerializer(data=request.data) # Deserialize the incoming data
        if serialiser.is_valid():
            serialiser.save() # Save the new product to the database
            return Response(serialiser.data, status=status.HTTP_201_CREATED) # Return success response
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST) # Return validation errors

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk) # Attempt to retrieve the product by its primary key
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) # If not found, return 404 error
    
    if request.method == 'GET': # retrieve the details of the specific product
        serialiser = ProductSerializer(product) # Serialize the product data
        return Response(serialiser.data) # Return the serialized product data
    
    if request.method == 'PUT': # update the product with the data provided in the request
        serialiser = ProductSerializer(product, data=request.data) # Deserialize and update product with incoming data
        if serialiser.is_valid():
            serialiser.save() # Save the updated product to the database
            return Response(serialiser.data) # Return the updated product data
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE': # Delete the product
        product.delete() # Delete the product from the database
        return Response(status=status.HTTP_204_NO_CONTENT) # Return 204 No Content to indicate successful deletion


@csrf_exempt  # Temporarily exempt from CSRF for simplicity
def contact_submission(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Send an email to admin
        send_mail(
            subject=f"Contact Form Submission: {subject}",
            message=f"Message from {name} ({email}):\n\n{message}",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= ['codepulse01@gmail.com'],
            fail_silently=False,
        )

        # Send an email to user
        send_mail(
            subject=f"We received your message!",
            message=f"Thank you for reaching out. We will get back to you shortly.",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= [email],
            fail_silently=False,
        )


        return JsonResponse({"success": True, "message": "Email sent successfully!"})
    return JsonResponse({"error": "Invalid request method."}, status=400)


