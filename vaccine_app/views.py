from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import date
from dateutil.relativedelta import relativedelta
from .models import Child, Vaccine, VaccinationRecord
from .forms import LookupForm, ChildForm


def index(request):
    """Front page with lookup form"""
    form = LookupForm()
    child = None
    not_found = False
    
    if request.method == 'POST':
        form = LookupForm(request.POST)
        if form.is_valid():
            search_value = form.cleaned_data['search_value']
            # Search by RCH number or parent number
            try:
                child = Child.objects.get(
                    Q(rch_number__iexact=search_value) | 
                    Q(parent_number=search_value)
                )
                return redirect('child_details', child_id=child.id)
            except Child.DoesNotExist:
                not_found = True
            except Child.MultipleObjectsReturned:
                # If multiple children with same parent number, show all
                children = Child.objects.filter(parent_number=search_value)
                return render(request, 'vaccine_app/children_list.html', {
                    'children': children,
                    'search_value': search_value
                })
    
    return render(request, 'vaccine_app/index.html', {
        'form': form,
        'not_found': not_found
    })


def register_child(request):
    """Register a new child"""
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save()
            # Create vaccination schedule for the child
            create_vaccination_schedule(child)
            messages.success(request, f'Child {child.child_name} registered successfully!')
            return redirect('vaccination_schedule', child_id=child.id)
    else:
        form = ChildForm()
    
    return render(request, 'vaccine_app/child_form.html', {
        'form': form,
        'title': 'Register New Child'
    })


def child_details(request, child_id):
    """View and edit child details"""
    child = get_object_or_404(Child, id=child_id)
    
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, 'Child details updated successfully!')
            return redirect('child_details', child_id=child.id)
    else:
        form = ChildForm(instance=child)
    
    return render(request, 'vaccine_app/child_form.html', {
        'form': form,
        'child': child,
        'title': 'Child Details'
    })


def vaccination_schedule(request, child_id):
    """Display vaccination schedule for a child"""
    child = get_object_or_404(Child, id=child_id)
    
    # Update statuses
    for record in child.vaccination_records.all():
        old_status = record.status
        new_status = record.update_status()
        if old_status != new_status:
            record.save()
    
    # Get all vaccination records
    records = child.vaccination_records.all().select_related('vaccine')
    
    # Separate by status
    completed = records.filter(status='completed')
    pending = records.filter(status='pending')
    overdue = records.filter(status='overdue')
    
    return render(request, 'vaccine_app/vaccination_schedule.html', {
        'child': child,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'all_records': records
    })


def mark_vaccine_administered(request, record_id):
    """Mark a vaccine as administered"""
    record = get_object_or_404(VaccinationRecord, id=record_id)
    
    if request.method == 'POST':
        record.administered_date = date.today()
        record.status = 'completed'
        record.save()
        messages.success(request, f'{record.vaccine.name} marked as administered!')
    
    return redirect('vaccination_schedule', child_id=record.child.id)


def create_vaccination_schedule(child):
    """Create vaccination records for a child based on available vaccines"""
    vaccines = Vaccine.objects.all()
    
    for vaccine in vaccines:
        # Calculate scheduled date based on child's DOB and vaccine's recommended age
        scheduled_date = child.date_of_birth + relativedelta(months=vaccine.recommended_age_months)
        
        # Determine initial status
        today = date.today()
        if scheduled_date < today:
            status = 'overdue'
        else:
            status = 'pending'
        
        VaccinationRecord.objects.get_or_create(
            child=child,
            vaccine=vaccine,
            defaults={
                'scheduled_date': scheduled_date,
                'status': status
            }
        )
