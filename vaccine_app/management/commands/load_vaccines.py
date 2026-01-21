from django.core.management.base import BaseCommand
from vaccine_app.models import Vaccine


class Command(BaseCommand):
    help = 'Load initial vaccine data into the database'

    def handle(self, *args, **options):
        vaccines = [
            {'name': 'BCG', 'recommended_age_months': 0, 'description': 'Bacillus Calmette-Guérin - protects against tuberculosis'},
            {'name': 'Hepatitis B (Birth dose)', 'recommended_age_months': 0, 'description': 'First dose of Hepatitis B vaccine'},
            {'name': 'OPV-0', 'recommended_age_months': 0, 'description': 'Oral Polio Vaccine - birth dose'},
            {'name': 'OPV-1', 'recommended_age_months': 2, 'description': 'Oral Polio Vaccine - first dose'},
            {'name': 'Pentavalent-1', 'recommended_age_months': 2, 'description': 'DPT + Hepatitis B + Hib - first dose'},
            {'name': 'Rotavirus-1', 'recommended_age_months': 2, 'description': 'Rotavirus vaccine - first dose'},
            {'name': 'PCV-1', 'recommended_age_months': 2, 'description': 'Pneumococcal Conjugate Vaccine - first dose'},
            {'name': 'OPV-2', 'recommended_age_months': 4, 'description': 'Oral Polio Vaccine - second dose'},
            {'name': 'Pentavalent-2', 'recommended_age_months': 4, 'description': 'DPT + Hepatitis B + Hib - second dose'},
            {'name': 'Rotavirus-2', 'recommended_age_months': 4, 'description': 'Rotavirus vaccine - second dose'},
            {'name': 'OPV-3', 'recommended_age_months': 6, 'description': 'Oral Polio Vaccine - third dose'},
            {'name': 'Pentavalent-3', 'recommended_age_months': 6, 'description': 'DPT + Hepatitis B + Hib - third dose'},
            {'name': 'Rotavirus-3', 'recommended_age_months': 6, 'description': 'Rotavirus vaccine - third dose'},
            {'name': 'PCV-2', 'recommended_age_months': 6, 'description': 'Pneumococcal Conjugate Vaccine - second dose'},
            {'name': 'Measles-1', 'recommended_age_months': 9, 'description': 'Measles vaccine - first dose'},
            {'name': 'Vitamin A (1st dose)', 'recommended_age_months': 9, 'description': 'Vitamin A supplementation'},
            {'name': 'MR-1 (Measles-Rubella)', 'recommended_age_months': 12, 'description': 'Measles and Rubella vaccine - first dose'},
            {'name': 'JE-1', 'recommended_age_months': 12, 'description': 'Japanese Encephalitis - first dose'},
            {'name': 'PCV Booster', 'recommended_age_months': 12, 'description': 'Pneumococcal Conjugate Vaccine - booster'},
            {'name': 'DPT Booster-1', 'recommended_age_months': 18, 'description': 'DPT booster - first dose'},
            {'name': 'OPV Booster', 'recommended_age_months': 18, 'description': 'Oral Polio Vaccine - booster'},
            {'name': 'MR-2 (Measles-Rubella)', 'recommended_age_months': 18, 'description': 'Measles and Rubella vaccine - second dose'},
            {'name': 'JE-2', 'recommended_age_months': 24, 'description': 'Japanese Encephalitis - second dose'},
            {'name': 'DPT Booster-2', 'recommended_age_months': 60, 'description': 'DPT booster - second dose (5 years)'},
        ]

        created_count = 0
        for vax_data in vaccines:
            vaccine, created = Vaccine.objects.get_or_create(
                name=vax_data['name'],
                defaults={
                    'recommended_age_months': vax_data['recommended_age_months'],
                    'description': vax_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Created: {vaccine.name}')
            else:
                self.stdout.write(f'  Already exists: {vaccine.name}')

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded {created_count} new vaccines'))
