from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.db import transaction
from .models import CustomUser, Usermember
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = request.POST
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            username = data.get('username')
            email = data.get('email')
            mobile = data.get('mobile')
            password = data.get('password')
            age = data.get('age')
            address = data.get('address')
            logo = request.FILES.get('logo')

            if not email or not password or not username or not first_name or not last_name or not age or not address:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email is already taken.'}, status=400)

            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username is already taken.'}, status=400)

            with transaction.atomic():
                user = CustomUser(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=make_password(password),
                    user_type=2
                )
                user.save()

                user_member = Usermember(
                    user=user,
                    age=age,
                    number=mobile,  
                    address=address,
                    image=logo  # Ensure the correct field is used
                )
                user_member.save()

            return JsonResponse({'success': 'User created successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def signup2(request):
    if request.method == 'POST':
        # Extract data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        logo = request.FILES.get('logo')

        # Check if required fields are present
        if not all([first_name, last_name, username, mobile, email, password, confirm_password, logo]):
            return JsonResponse({'error': 'Please fill in all fields.'}, status=400)

        # Check if passwords match
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        try:
            # Create CustomUser instance with user_type=3 for delivery user
            user = CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=make_password(password),  # Ensure the password is hashed
                user_type=3  # Assuming user_type 3 corresponds to delivery user
            )

            # Create Usermember instance linked to CustomUser
            Usermember.objects.create(
                user=user,
                number=mobile,
                image=logo  # Assuming 'image' field in Usermember model corresponds to logo
            )

            return JsonResponse({'message': 'Signup successful.' }, status=201)

        except Exception as e:
            return JsonResponse({'error': f'Signup failed. {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = request.POST or json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required.'}, status=400)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                user_type = user.user_type  # Assuming user_type is a field in your user model

                if user_type == '2':  # Client
                    return JsonResponse({'message': 'Login successful', 'redirect': 'client_dashboard'}, status=200)
                elif user_type == '3':  # Delivery user
                    return JsonResponse({'message': 'Login successful', 'redirect': 'delivery_dashboard'}, status=200)
                elif user.is_superuser:  # Admin
                    return JsonResponse({'message': 'Login successful', 'redirect': 'admin_dashboard'}, status=200)
                else:
                    return JsonResponse({'error': 'Unexpected user type.'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def profile(request):
    user = request.user  # Assuming user is authenticated
    
    try:
        usermember = Usermember.objects.get(user=user)
        
        profile_data = {
            'name': usermember.user.username,
            'email': user.email,
            'imageUrl': usermember.image.url if usermember.image else None  # Assuming image is an ImageField
        }
        
        return JsonResponse(profile_data)
    
    except Usermember.DoesNotExist:
        # Handle case where Usermember does not exist for the user
        profile_data = {
            'name': user.username,
            'email': user.email,
            'imageUrl': None
        }
        
        return JsonResponse(profile_data)
