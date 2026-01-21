from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta


class Child(models.Model):
    """Primary details of a child"""
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    rch_number = models.CharField(max_length=20, unique=True, verbose_name="RCH Number")
    parent_number = models.CharField(max_length=15, verbose_name="Parent Number")
    child_name = models.CharField(max_length=100, verbose_name="Child Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name="Sex")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Children"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.child_name} ({self.rch_number})"
    
    @property
    def age_in_months(self):
        """Calculate age in months from date of birth"""
        today = date.today()
        delta = relativedelta(today, self.date_of_birth)
        return delta.years * 12 + delta.months
    
    @property
    def age_display(self):
        """Display age in a readable format"""
        months = self.age_in_months
        if months < 12:
            return f"{months} months"
        years = months // 12
        remaining_months = months % 12
        if remaining_months == 0:
            return f"{years} year{'s' if years > 1 else ''}"
        return f"{years} year{'s' if years > 1 else ''}, {remaining_months} month{'s' if remaining_months > 1 else ''}"


class Vaccine(models.Model):
    """Vaccine information"""
    name = models.CharField(max_length=100, verbose_name="Vaccine Name")
    recommended_age_months = models.IntegerField(verbose_name="Recommended Age (months)")
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        ordering = ['recommended_age_months', 'name']
    
    def __str__(self):
        return f"{self.name} (at {self.recommended_age_months} months)"


class VaccinationRecord(models.Model):
    """Record of vaccination for a child"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccination_records')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    scheduled_date = models.DateField(verbose_name="Scheduled Date")
    administered_date = models.DateField(null=True, blank=True, verbose_name="Administered Date")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['scheduled_date']
        unique_together = ['child', 'vaccine']
    
    def __str__(self):
        return f"{self.child.child_name} - {self.vaccine.name} ({self.status})"
    
    def update_status(self):
        """Update status based on dates"""
        today = date.today()
        if self.administered_date:
            self.status = 'completed'
        elif self.scheduled_date < today:
            self.status = 'overdue'
        else:
            self.status = 'pending'
        return self.status
