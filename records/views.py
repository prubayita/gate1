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

# @login_required
# @group_required('Security')
def record_visitor(request):
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
    return render(request, 'records/test.html')

@login_required
def check_out_visitor(request, visitor_id):
    # movement = Movement.objects.get(pk=visitor_id)
    movement = get_object_or_404(Movement, visitor__id_passport_nbr=visitor_id, time_out__isnull=True)
    # if movement.time_out is None:
    movement.time_out = datetime.now()
    movement.save()
    messages.success(request, 'Visitor checked out successfully.')
    return redirect('records:movements')

@login_required
# @group_required('Supervisor')
# @group_required('Security')
def visitor_list(request):
    waitinglist=WaitingList.objects.all().values()
    template = loader.get_template('records/visitor_list.html')
    context = {'waitinglist': waitinglist }
    return HttpResponse(template.render(context, request))

# details of a visitor
def details(request, visitor_id):
    detailedVisitor = get_object_or_404(WaitingList, id_passport_nbr=visitor_id)
    
    # Handle form submission for visitor approval
    if request.method == 'POST':
        # Get the form data
        purpose = request.POST.get('purpose')
        comment = request.POST.get('comment')
        card_id = request.POST.get('card')
        devices = request.POST.get('devices')
        
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
            comment=comment
        )
        
        # Set the card if selected
        if card_id:
            card = get_object_or_404(Card, pk=card_id)
            movement.card = card
        
        # Save the Movement instance
        movement.save()
        
        # Redirect or render a success message
        detailedVisitor.delete()
        return redirect('records:visitors')
    # Render the details template with the visitor's information
    context = {
        'detailedVisitor': detailedVisitor,
    }
    return render(request, 'records/visitor_list.html', context)
#   detailedVisitor = WaitingList.objects.get(id_passport_nbr=id)
#   template = loader.get_template('records/details.html')
#   context = {
#     'detailedVisitor': detailedVisitor,
#   }
#   return HttpResponse(template.render(context, request))

@login_required
def search_visitors(request):
    query = request.GET.get('query', '')
    visitors = Visitor.objects.filter(first_name__icontains=query)
    context = {'visitors': visitors}
    html = render_to_string('records/search_results.html', context)
    return JsonResponse({'html': html})



def approve_visitor(request, visitor_id):
    # Retrieve the visitor from the WaitingList
    waiting_visitor = WaitingList.objects.get(id_passport_nbr=visitor_id)

    # Create a new Visitor instance with the data from the WaitingList
    visitor = Visitor(
        id_passport_nbr=waiting_visitor.id_passport_nbr,
        first_name=waiting_visitor.first_name,
        surname=waiting_visitor.surname,
        organization=waiting_visitor.organization,
        position=waiting_visitor.position,
        country_of_origin=waiting_visitor.country_of_origin,
        email=waiting_visitor.email,
        address=waiting_visitor.address,
        mobile_phone=waiting_visitor.mobile_phone
    )

    # Save the new Visitor instance
    visitor.save()

    # Delete the corresponding entry from the WaitingList
    waiting_visitor.delete()
    messages.success(request, 'Visitor checked out successfully.')
    return redirect('records:visitors')


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