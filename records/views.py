from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import *
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .decorators import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import Log


def login(request):  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('records:record_visitor')  # Redirect to the desired page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('records:login')
    return render(request, 'cre/login.html')

def logout_view(request):
    logout(request)
    return redirect('records:login') 

def overview(request):
  template = loader.get_template('records/test.html')
  return HttpResponse(template.render())

@login_required
# @group_required('Security')
def record_visitor(request):
    visitors_list = Visitor.objects.all().values()
    visitors_list = json.dumps(list(visitors_list))
    if request.method == 'POST':
        form_data = request.POST
        waitingList = WaitingList(
            id_passport_nbr=form_data['id_passport_nbr'],
            first_name=form_data['first_name'],
            surname=form_data['surname'],
            organization=form_data['organization'],
            position=form_data['position'],
            country_of_origin=form_data['country_of_origin'],
            email=form_data['email'],
            address=form_data['address'],
            mobile_phone=form_data['mobile_phone'],
            # purpose=form_data['purpose'],
            # devices=form_data['devices'],
            # time_in=datetime.now()
        )
        waitingList.save()
        messages.success(request, 'Visitor recorded successfully in WaitingList.')
        return redirect('records:record_visitor')
    return render(request, 'records/test.html', {'visitors_list': visitors_list})

@login_required
def check_out_visitor(request, visitor_id):
    # Retrieve the movement with the provided visitor_id and time_out=None
    movement = get_object_or_404(Movement, visitor__id_passport_nbr=visitor_id, time_out__isnull=True)

    # Set the time_out to the current time and save the movement
    movement.time_out = timezone.now()
    movement.user_checked_out = request.user  # Assign the user who checked out the visitor
    movement.save()

    # Create a new Log entry to record the action
    log_entry = Log(action='CHECKOUT', user=request.user, visitor_id=visitor_id)
    log_entry.save()

    messages.success(request, 'Visitor checked out successfully.')
    return redirect('records:movements')
@login_required
def manual_checkout(request):
    if request.method == 'POST':
        card_number = request.POST['cardNumber']
        try:
            # Retrieve all matching Movement objects (unchecked-in movements with the given card number)
            movements = Movement.objects.filter(card__number=card_number, time_out__isnull=True)

            if movements.exists():
                # Choose the most recent Movement (based on id) for checkout
                movement = movements.latest('id')
                movement.time_out = timezone.now()
                movement.user_checked_out = request.user  # Assign the user who checked out the visitor
                movement.save()

                # Create a new Log entry to record the action
                log_entry = Log(action='CHECKOUT', user=request.user, visitor_id=movement.visitor_id)
                log_entry.save()

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid card number or visitor already checked out.'})
        except Movement.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid card number or visitor already checked out.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


# @group_required('Supervisor')
# @group_required('Security')
@login_required
def visitor_list(request):
    # Fetch the list of users
    users = User.objects.all()

    waitinglist = WaitingList.objects.all().values()
    cards = Card.objects.all().values()
    template = loader.get_template('records/visitor_list.html')
    context = {'waitinglist': waitinglist, 'cards': cards, 'users': users}  # Add 'users' to the context
    return HttpResponse(template.render(context, request))

@login_required
# details of a visitor
@login_required
def details(request, visitor_id):
    detailedVisitor = get_object_or_404(WaitingList, id_passport_nbr=visitor_id)

    if request.method == 'POST':
        # Get the form data
        purpose = request.POST.get('purpose')
        comment = request.POST.get('comment')
        devices = request.POST.get('devices')
        card_number = request.POST.get('card')
        email_recipient_user = request.POST.get('email_recipient_user')

        # Create a new Visitor instance
        visitor = Visitor(
            id_passport_nbr=detailedVisitor.id_passport_nbr,
            first_name=detailedVisitor.first_name,
            surname=detailedVisitor.surname,
            organization=detailedVisitor.organization,
            position=detailedVisitor.position,
            country_of_origin=detailedVisitor.country_of_origin,
            email=detailedVisitor.email,
            address=detailedVisitor.address,
            mobile_phone=detailedVisitor.mobile_phone
        )
        # Save the Visitor instance
        visitor.save()

        # Create a new Movement instance
        movement = Movement(
            visitor=visitor,
            purpose=purpose,
            devices=devices,
            time_in=timezone.now(),
            comment=comment,
            card=None  # Set the card later, if selected
        )

        # Set the card if selected
        if card_number:
            card = Card.objects.filter(number=card_number).first()
            if card is not None:
                movement.card = card

        # Save the Movement instance
        movement.save()
        # Create a new Log entry to record the action of approving a visitor
        log_entry = Log(action='APPROVE', user=request.user, visitor_id=visitor_id)
        log_entry.save()
        # Send email notification to the selected user
        if email_recipient_user:
            user = User.objects.filter(username=email_recipient_user).first()
            if user is not None:
                subject = 'Visitor Approval Notification'
                message = f'Hello {user.username},\n\nYou have a visitor approved. Visitor details:\nName: {visitor.first_name} {visitor.surname}\nEmail: {visitor.email}\nPhone: {visitor.mobile_phone}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]

                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                except Exception as e:
                    # Handle any errors that might occur while sending the email
                    print(f"Error sending email: {e}")

        # Redirect or render a success message
        detailedVisitor.delete()
        messages.success(request, 'Visitor approved and email notification sent successfully.')
        return redirect('records:visitors')

    # Retrieve the list of BSC users for the dropdown
    users = User.objects.all()

    # Render the details template with the visitor's information and users list
    context = {
        'detailedVisitor': detailedVisitor,
        'users': users,
    }
    return render(request, 'records/visitor_list.html', context)
#   detailedVisitor = WaitingList.objects.get(id_passport_nbr=id)
#   template = loader.get_template('records/details.html')
#   context = {
#     'detailedVisitor': detailedVisitor,
#   }
#   return HttpResponse(template.render(context, request))
@login_required
# decline in waiting list 
def delete_waiting(request, visitor_id):
    waiting_list = get_object_or_404(WaitingList, id_passport_nbr=visitor_id)
    # Create a new Log entry to record the action of approving a visitor
    log_entry = Log(action='DECLINE', user=request.user, visitor_id=visitor_id)
    log_entry.save()
    if request.method == 'POST':
        waiting_list.delete()
        return redirect('records:visitors')  # Redirect to the list of visitors after successful deletion

    
    # You can also handle the case when the request method is not POST, e.g., show a confirmation page.
    # In this example, it simply redirects to the list of visitors.
    messages.success(request, 'Visitor declined successfully.')
    return redirect('records:visitors')

@login_required
def search_visitors(request):
    query = request.GET.get('query', '')
    visitors = Visitor.objects.filter(first_name__icontains=query)
    context = {'visitors': visitors}
    html = render_to_string('records/search_results.html', context)
    return JsonResponse({'html': html})


# @login_required
# def approve_visitor(request, visitor_id):
#     # Get the selected user's username from the form data
#     selected_user = request.POST.get('email_recipient_user')
#     # Retrieve the visitor from the WaitingList
#     waiting_visitor = WaitingList.objects.get(id_passport_nbr=visitor_id)

#     # Create a new Visitor instance with the data from the WaitingList
#     visitor = Visitor(
#         id_passport_nbr=waiting_visitor.id_passport_nbr,
#         first_name=waiting_visitor.first_name,
#         surname=waiting_visitor.surname,
#         organization=waiting_visitor.organization,
#         position=waiting_visitor.position,
#         country_of_origin=waiting_visitor.country_of_origin,
#         email=waiting_visitor.email,
#         address=waiting_visitor.address,
#         mobile_phone=waiting_visitor.mobile_phone
#     )

#     # Save the new Visitor instance
#     visitor.save()

#     # Create a new Log entry to record the action of approving a visitor
#     log_entry = Log(action='APPROVE', user=request.user, visitor_id=visitor_id)
#     log_entry.save()

#     # Send an email to the selected user
#     user_email = User.objects.get(username=selected_user).email
#     subject = 'Visitor Approval Notification'
#     message = f'Hello {selected_user},\n\nYou have a visitor waiting for approval.\n\nPlease login to the system to approve the visitor.\n\nBest regards,\nThe Visitor Management Team'
#     from_email = 'visitor@bsc.rw'  # Replace with your email address or a no-reply email address
#     recipient_list = [user_email]
    
#     # Send the email
#     send_mail(subject, message, from_email, recipient_list)

#     # Delete the corresponding entry from the WaitingList
#     waiting_visitor.delete()

#     messages.success(request, 'Visitor approved successfully.')
#     return redirect('records:visitors')

@login_required
def movements(request):
    # movements = Movement.objects.all()
    checked_in_visitors = Movement.objects.filter(time_out__isnull=True)
    checked_out_visitors = Movement.objects.exclude(time_out__isnull=True)

    # Order checked-in visitors by most recent first
    checked_in_visitors = checked_in_visitors.order_by('-id')

    # Order checked-out visitors by most recent checked-out time
    checked_out_visitors = checked_out_visitors.order_by('-time_out')

    movements = list(checked_in_visitors) + list(checked_out_visitors)
    context = {'movements': movements}
    
    return render(request, 'records/movement.html', context)
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        # Create a new user in the database
        try:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.is_staff = True
            user.is_superuser = True
            user.save()

            # Automatically log in the new user
            auth_login(request, user)

            # Redirect to the desired page after successful signup (e.g., record_visitor page)
            return redirect('records:record_visitor')
        except Exception as e:
            messages.error(request, 'Error creating user. Please try again.')
            # Redirect back to the signup page
            return redirect('records:signup')

    return render(request, 'cre/signup.html')

@login_required
def logs(request):
    # Query the Log model and order the logs by timestamp in descending order (most recent first)
    logs = Log.objects.all().order_by('-timestamp')

    context = {'logs': logs}
    return render(request, 'records/logs.html', context)