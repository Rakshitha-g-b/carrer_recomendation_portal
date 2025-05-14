# File: career_guidance_system/recommender/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import State, City, StreamTag # <<< ADD THIS IMPORT LINE

class CustomUserCreationForm(UserCreationForm):
    # ... (your existing CustomUserCreationForm code) ...
    email = forms.EmailField(
        required=True,
        help_text='Required. Please provide a valid email address.'
    )
    first_name = forms.CharField(
        max_length=150, 
        required=True,
        help_text='Required.'
    )
    last_name = forms.CharField(
        max_length=150, 
        required=True,
        help_text='Required.'
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')


class RecommendationInputForm(forms.Form):
    # ... (your existing RecommendationInputForm code with percentage, interests, and quiz) ...
    percentage = forms.FloatField(
        label="Your 10th Grade Percentage (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'e.g., 75.5'})
    )
    INTEREST_CHOICES_ACTIVITY = [
        ('', '---------'),
        ('problem_solving', 'Solving Puzzles / Building Things / Technical Tasks'),
        ('business_finance', 'Understanding Money / Businesses / Organizing'),
        ('creative_expression', 'Reading / Writing / Art / Performing'),
        ('helping_understanding', 'Helping People / Understanding Behavior / Social Issues'),
    ]
    activity_interest = forms.ChoiceField(
        label="Which of these activities do you enjoy most?",
        choices=INTEREST_CHOICES_ACTIVITY,
        widget=forms.Select(attrs={'class': 'form-select mb-3'}),
        required=True
    )
    INTEREST_CHOICES_SUBJECT_TYPE = [
        ('', '---------'),
        ('analytical_logical', 'Analytical & Logical Subjects (Math, Physics)'),
        ('theoretical_memorization', 'Theoretical & Information-rich Subjects (History, Biology concepts)'),
        ('practical_application', 'Practical & Application-oriented Subjects (Lab work, Economics application)'),
        ('language_communication', 'Language & Communication-focused Subjects (Literature, Debate)'),
    ]
    subject_type_preference = forms.ChoiceField(
        label="What type of subjects or learning style do you prefer?",
        choices=INTEREST_CHOICES_SUBJECT_TYPE,
        widget=forms.Select(attrs={'class': 'form-select mb-3'}),
        required=True
    )
    QUIZ_Q1_CHOICES = [
        ('', '---------'),
        ('q1_a', 'Break it down logically and find a systematic solution.'),
        ('q1_b', 'Think about practical implications and resources/people.'),
        ('q1_c', 'Explore different perspectives and creative approaches.'),
        ('q1_d', 'Discuss with others to understand different viewpoints.'),
    ]
    quiz_q1 = forms.ChoiceField(
        label="When faced with a new, complex problem, I tend to first:",
        choices=QUIZ_Q1_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    QUIZ_Q2_CHOICES = [
        ('', '---------'),
        ('q2_a', 'Innovation, technology, and discovery.'),
        ('q2_b', 'Strategy, management, and financial growth.'),
        ('q2_c', 'Expression, communication, and cultural understanding.'),
        ('q2_d', 'Direct interaction with people and societal impact.'),
    ]
    quiz_q2 = forms.ChoiceField(
        label="I'm more drawn to careers that involve:",
        choices=QUIZ_Q2_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    QUIZ_Q3_CHOICES = [
        ('', '---------'),
        ('q3_a', 'Deep research and precise calculations.'),
        ('q3_b', 'Planning, execution, and achieving business outcomes.'),
        ('q3_c', 'Self-expression and making an artistic/intellectual statement.'),
        ('q3_d', 'Understanding and improving human or societal conditions.'),
    ]
    quiz_q3 = forms.ChoiceField(
        label="If I had to choose a long-term project, I'd prefer something that:",
        choices=QUIZ_Q3_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )


class CollegeSearchForm(forms.Form):
    state = forms.ModelChoiceField(
        queryset=State.objects.all().order_by('name'),
        empty_label="-- Select State --",
        widget=forms.Select(attrs={'class': 'form-select mb-2', 'id': 'id_state_search'})
    )
    city = forms.ModelChoiceField( 
        queryset=City.objects.none(), # queryset will be updated by JS based on state selection
        empty_label="-- Select City (after state) --",
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select mb-2', 'id': 'id_city_search'})
    )
    stream = forms.ModelChoiceField(
        queryset=StreamTag.objects.all().order_by('name'),
        empty_label="-- Select Stream (Optional) --",
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select mb-3'})
    )