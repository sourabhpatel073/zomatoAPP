from django.shortcuts import render
from django.contrib.auth.hashers import check_password
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Dish, Order,Notification
from .serializers import DishSerializer
from .serializers import OrderSerializer
from .serializers import NotificationSerializer

from rest_framework.permissions import AllowAny
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer

from django.contrib.auth import authenticate, login
import openai
from .models import Feedback
from .serializers import FeedbackSerializer

openai.api_key = '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'

@api_view(['GET'])
def display_menu(request):
    dishes = Dish.objects.all()
    serializer = DishSerializer(dishes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_dish(request):
    serializer = DishSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def update_dish_availability(request, dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
    except Dish.DoesNotExist:
        return Response(status=404)

    serializer = DishSerializer(dish, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_dish(request, dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
    except Dish.DoesNotExist:
        return Response(status=404)
    dish.delete()
    return Response(status=204)



@api_view(['GET'])
def display_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def place_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=404)

    old_status = order.status
    serializer = OrderSerializer(order, data=request.data, partial=True)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer.save()

    if old_status != serializer.data["status"]:
        # Preparing the WebSocket message when the order status changes
        channel_layer = get_channel_layer()
        notification_content = {
            'type': 'order_status',
            'order_id': order.id,
            "userNo": 1,
            'new_status': serializer.data["status"],
            'message': f" {order.customer_name} your Order {order.id} status -  changed to {serializer.data['status']}"
        }
        # Sending the message to the 'notifications' group via WebSocket
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                'type': 'order_status',
                'message': notification_content
            }
        )
    
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(status=404)
    order.delete()
    return Response(status=204)

# ----------------------------------------------------------------------chatbot----------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def process_chatbot_message(request):
    user_message = request.data.get('message', '').lower()  # Extracting message from the request

    # Greeting response
    if "hello" in user_message or "hi" in user_message:
        return Response({"response": "Hello! Welcome to our Food Delivery App. How can I assist you today?"})
    elif "who are you" in user_message:
        return "I am the Food Delivery Chatbot, here to assist you with your orders and queries."
    # If user asks for the menu
    elif any(term in user_message for term in ["menu", "dishes", "item", "special"]):
        dishes = Dish.objects.all()
        if dishes:
                    menu_list = [dish.dish_name for dish in dishes if dish.availability]
                    menu_string = ", ".join(menu_list)
                    return Response({"response": f"Here are the available dishes: {menu_string}"})
        return Response({"response": f"Here are the available dishes: Indian,Chainies etc"})
    # Other general predefined queries

    elif any(term in user_message for term in ["order", "location", "payment", "time"]):
     return Response({"response": f"We as a team trying to optimize our servies , without any problem and exta fee or money"})


    responses = {
    "what kind of food you have": "We have various kinds of food like Indian, Chinese, and more."  , 
    "how does this work?": "You can search for restaurants, choose your favorite food, and place an order. We'll deliver it to your doorstep!",
    "what is the delivery charge?": "Delivery charges vary based on the restaurant and your location.",
    "how can i track my order?": "Once you place an order, you'll receive a tracking link via SMS and email.",
    "how long does delivery take?": "Usually, it takes 30-45 minutes, but it can vary based on the restaurant and your location.",
    "do you have any discounts?": "Yes! We often have discounts and offers. Check out our 'Offers' section.",
    "can i schedule an order?": "Absolutely! While placing an order, you can set a desired delivery time.",
    "is there a minimum order amount?": "Minimum order amount varies based on the restaurant.",
    "how do i report an issue with my order?": "You can report any issues via our app's 'Help' section or contact our customer service.",
    "do you offer vegetarian options?": "Yes, we do. You can filter restaurants by 'Vegetarian' in our app.",
    "can i cancel my order?": "Orders can be canceled within 5 minutes of placing them. After that, charges might apply.",
    "what payment methods do you accept?": "We accept credit cards, digital wallets, UPI, and cash on delivery.",
    "is my information safe with you?": "Yes, we prioritize user privacy and ensure your data is securely stored.",
    "can i order from multiple restaurants?": "You would need to place separate orders for different restaurants.",
    "do you have a referral program?": "Yes! You can refer friends and earn rewards when they place their first order.",
    "where do you operate?": "We operate in multiple cities across the country. Check our app for availability in your location.",
    "how can i contact the delivery person?": "After placing the order, you will receive the delivery person's contact details via SMS.",
    "what if i received the wrong order?": "Apologies for that. Please report it through the app and we will rectify it.",
    "how do i update my address?": "You can update your address in the 'Profile' section of our app.",
    "do you have gluten-free options?": "Yes, many of our partner restaurants offer gluten-free dishes. You can use the filter option to find them.",
    "are there any ongoing promotions?": "All ongoing promotions are listed under the 'Offers' tab in our app.",
}

    response = responses.get(user_message,"i")
    if response !="i":
        return Response({"response": response})
    

    else:
        
        prompt = f"A user on a food delivery platform states: {user_message}. Provide a direct and concise reply from the Food Delivery Chatbot ,do not give conversation your role is chatbot,here are some examples"

        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=10,  # Limiting response length
                n=1,
                temperature=0.1
            )
            chatbot_response = response.choices[0].text.strip()

            unrelated_phrases = ["pm of india", "politics", "history of", "science of"]
            if any(phrase in chatbot_response.lower() for phrase in unrelated_phrases):
                return Response({"response": "I'm not sure about that. Can you please clarify or ask something related to food or our services?"})

            return Response({"response": chatbot_response})

        except Exception as e:
            return Response({"response": "Sorry, I'm having some trouble understanding that. Please try again."})
            

    
        




# =========-----------------------------------------notification-----------------------------------
# views.py
@api_view(['POST'])
def save_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_notifications(request):
    notifications = Notification.objects.all().order_by('-timestamp')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_notification(request, notif_id):
    try:
        notification = Notification.objects.get(id=notif_id)
    except Notification.DoesNotExist:
        return Response(status=404)
    notification.delete()
    return Response(status=204)
# =================================user========================
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            profile = UserProfile.objects.create(user=user, name=request.data.get("name"))
            profile_serializer = UserProfileSerializer(profile, many=False)
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["POST"])
def login_view(request):
    try:
        # Fetching the email from request data
        email = request.data["email"]

        # Checking if the email exists in the database
        user_profile = UserProfile.objects.get(user__email=email)
        user_id = user_profile.user.id
        if user_profile:
            # Return a success response if the email exists
            
            return JsonResponse({"message": "Email found in database!","token":101, "user_id": user_id}, status=200)
        else:
            # Return a failure response if the email does not exist
            return JsonResponse({"message": "Email not found!"}, status=404)
    except UserProfile.DoesNotExist:
        # Return a failure response if the email does not exist
        return JsonResponse({"message": "Email not found!"}, status=404)
    except Exception as e:
        # Return a failure response if any exception occurs
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)
    

@api_view(['POST'])
def feedback_view(request):
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def get_all_feedbacks(request):
    feedbacks = Feedback.objects.all()
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)       