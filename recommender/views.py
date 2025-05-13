# File: career_guidance_system/recommender/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, RecommendationInputForm, CollegeSearchForm
from .models import College, City, State, StreamTag # Ensure these models exist and are created via migrations

# --- Stream Data ---
STREAM_INFO = {
    "Science": {
        "description": "Focuses on Physics, Chemistry, Mathematics/Biology. Prepares for engineering, medical, research fields.",
        "benefits": ["Develops analytical and problem-solving skills.","Wide range of higher education options (Engineering, Medical, BSc, etc.).","Foundation for research and innovation."],
        "opportunities": ["Engineer (Software, Mechanical, Civil, etc.)","Doctor, Dentist, Pharmacist","Scientist, Researcher","Architect","Pilot"],
        "salary_expectation": "Varies widely. Entry-level for engineers/doctors can be moderate to high, growing significantly with experience. Research salaries depend on funding and field."
    },
    "Commerce": {
        "description": "Focuses on Accountancy, Business Studies, Economics. Prepares for careers in finance, business, management.",
        "benefits": ["Develops understanding of business and financial systems.","Good for aspiring entrepreneurs and managers.","Options like CA, CS, BBA, B.Com."],
        "opportunities": ["Chartered Accountant (CA)","Company Secretary (CS)","Banker, Financial Analyst","Business Manager, Marketing Manager","Economist"],
        "salary_expectation": "Good potential. CAs, MBAs from top schools can earn very well. Banking and finance roles offer competitive salaries."
    },
    "Arts/Humanities": {
        "description": "Focuses on subjects like History, Political Science, Literature, Psychology, Sociology. Prepares for diverse fields including civil services, law, journalism, arts.",
        "benefits": ["Develops critical thinking, communication, and creative skills.","Broad understanding of society and human behavior.","Pathways to Law, Journalism, Civil Services, Teaching, Design."],
        "opportunities": ["Lawyer, Judge","Journalist, Editor","Civil Servant (IAS, IPS, etc.)","Teacher, Professor","Psychologist, Counselor","Designer (Graphic, Fashion, etc.)"],
        "salary_expectation": "Highly variable. Top lawyers, journalists, or successful civil servants earn very well. Other fields might start lower but offer job satisfaction and growth."
    }
}
# --- END Stream Data ---

# --- Resource Data ---
STREAM_RESOURCES = {
    "Science": {
        "General Information & Learning": [{"name": "NCERT Science Textbooks", "url": "https://ncert.nic.in/textbook.php"},{"name": "Khan Academy - Science", "url": "https://www.khanacademy.org/science"},{"name": "BYJU'S - Science Concepts", "url": "https://byjus.com/cbse/science/"},],
        "Career Portals & Further Study": [{"name": "National Career Service (India)", "url": "https://www.ncs.gov.in/"},{"name": "Shiksha.com - Science Courses", "url": "https://www.shiksha.com/science-courses-chp"},]
    },
    "Commerce": {
        "General Information & Learning": [{"name": "NCERT Commerce Textbooks", "url": "https://ncert.nic.in/textbook.php"},{"name": "Investopedia - Commerce Basics", "url": "https://www.investopedia.com/"},{"name": "Toppr - Commerce Study Material", "url": "https://www.toppr.com/guides/commerce/"},],
        "Professional Bodies & Career Info": [{"name": "ICAI (Chartered Accountants)", "url": "https://www.icai.org/"},{"name": "ICSI (Company Secretaries)", "url": "https://www.icsi.edu/"},{"name": "CollegeDunia - B.Com Colleges", "url": "https://collegedunia.com/bcom-colleges"},]
    },
    "Arts/Humanities": {
        "General Information & Learning": [{"name": "NCERT Humanities Textbooks", "url": "https://ncert.nic.in/textbook.php"},{"name": "Project Gutenberg (Literature)", "url": "https://www.gutenberg.org/"},{"name": "Coursera - Humanities Courses", "url": "https://www.coursera.org/browse/humanities"},],
        "Career Exploration & Further Study": [{"name": "Careers360 - Arts Careers", "url": "https://www.careers360.com/careers/arts-humanities-and-social-sciences"},{"name": "IndiaToday - Career Choices in Arts", "url": "https://www.indiatoday.in/education-today/jobs-and-careers/story/career-choices-in-arts-stream-10-options-you-must-explore-after-class-12-1967099-2022-06-27"},]
    }
}
# --- END Resource Data ---

# --- Quiz Scoring Data ---
QUIZ_SCORES = {
    'q1': { 'q1_a': {'S': 2,   'C': 1,   'A': 0}, 'q1_b': {'S': 0.5, 'C': 2,   'A': 1}, 'q1_c': {'S': 0,   'C': 0.5, 'A': 2}, 'q1_d': {'S': 0,   'C': 1,   'A': 1.5},},
    'q2': { 'q2_a': {'S': 2,   'C': 0.5, 'A': 0}, 'q2_b': {'S': 0,   'C': 2,   'A': 0.5}, 'q2_c': {'S': 0,   'C': 0.5, 'A': 2}, 'q2_d': {'S': 1,   'C': 1,   'A': 1.5},},
    'q3': { 'q3_a': {'S': 2,   'C': 0.5, 'A': 0}, 'q3_b': {'S': 0,   'C': 2,   'A': 0.5}, 'q3_c': {'S': 0,   'C': 0,   'A': 2}, 'q3_d': {'S': 1,   'C': 0.5, 'A': 1.5},}
}
# --- END Quiz Scoring ---


def home_view(request):
    print("DEBUG: home_view called - rendering 'recommender/home.html'")
    return render(request, 'recommender/home.html')

def register_view(request):
    print("DEBUG: register_view called - attempting to render form or process POST")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"DEBUG: User {user.username} registered and logged in. Redirecting to congratulations.")
            return redirect('congratulations')
        else:
            print("DEBUG: Registration form is invalid with errors: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    print("DEBUG: login_view called - attempting to render form or process POST")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"DEBUG: User {username} logged in. Redirecting.")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
            else:
                print("DEBUG: Authentication failed for login.")
                form.add_error(None, "Invalid username or password. Please try again.")
        else:
            print(f"DEBUG: Login form is invalid with errors: {form.errors}")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def congratulations_view(request):
    print("DEBUG: congratulations_view called - rendering template")
    return render(request, 'recommender/congratulations.html')

def logout_view(request):
    user_display = request.user.username if request.user.is_authenticated else "AnonymousUser"
    print(f"DEBUG: logout_view called for user {user_display}")
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    user_display = request.user.username if request.user.is_authenticated else "AnonymousUser"
    print(f"DEBUG: dashboard_view called for user {user_display} with method {request.method}")
    
    SPECIAL_RECOMMENDATION_TYPES = ["NoClearRecommendation", "MultipleSuggestions"]
    
    recommendation_form = RecommendationInputForm() 
    college_search_form = CollegeSearchForm()   

    # Initialize context with all necessary data for GET requests
    processed_all_streams = {key: data.copy() for key, data in STREAM_INFO.items()}
    for stream_data_val in processed_all_streams.values():
        stream_data_val['show_in_accordion'] = True # Default to show

    context = {
        'form': recommendation_form,             
        'college_search_form': college_search_form, 
        'STREAM_RESOURCES': STREAM_RESOURCES,
        'all_streams': processed_all_streams, 
        'SPECIAL_RECOMMENDATION_TYPES': SPECIAL_RECOMMENDATION_TYPES,
        'recommendation_type': None, # Initialize for GET requests
        'recommendation_reasoning': [], # Initialize for GET requests
    }

    if request.method == 'POST':
        print("DEBUG: dashboard_view - POST request received for recommendation")
        recommendation_form = RecommendationInputForm(request.POST)
        context['form'] = recommendation_form # Update form in context with POST data

        if recommendation_form.is_valid():
            percentage = recommendation_form.cleaned_data['percentage']
            activity = recommendation_form.cleaned_data['activity_interest']
            subject_pref = recommendation_form.cleaned_data['subject_type_preference']
            q1_ans = recommendation_form.cleaned_data['quiz_q1']
            q2_ans = recommendation_form.cleaned_data['quiz_q2']
            q3_ans = recommendation_form.cleaned_data['quiz_q3']
            
            print(f"DEBUG --- Inputs ---")
            print(f"Percentage: {percentage}")
            print(f"Activity Interest: {activity}")
            print(f"Subject Preference: {subject_pref}")
            print(f"Quiz Q1: {q1_ans}, Q2: {q2_ans}, Q3: {q3_ans}")

            stream_scores = {"Science": 0, "Commerce": 0, "Arts/Humanities": 0}
            recommendation_reasoning = [] # Reset reasoning for new POST

            # 1. Percentage-based
            base_recommendation_perc = ""
            if percentage >= 85: stream_scores["Science"] += 2.5; base_recommendation_perc = "Science (strong)"
            elif percentage >= 75: stream_scores["Science"] += 1.5; stream_scores["Commerce"] += 1.0; base_recommendation_perc = "Science or Commerce"
            elif percentage >= 60: stream_scores["Commerce"] += 1.5; stream_scores["Science"] += 0.5; stream_scores["Arts/Humanities"] += 0.5; base_recommendation_perc = "Commerce or Arts/Science"
            elif percentage >= 45: stream_scores["Arts/Humanities"] += 1.5; stream_scores["Commerce"] += 0.5; base_recommendation_perc = "Arts or Commerce"
            else: stream_scores["Arts/Humanities"] += 2.5; base_recommendation_perc = "Arts/Humanities (strong)"
            if percentage > 0 : recommendation_reasoning.append(f"Your percentage ({percentage}%) suggests: {base_recommendation_perc}.")

            # 2. Activity Interest
            activity_reason_map = {
                'problem_solving': "Interest in problem-solving/technical tasks aligns with Science and some Commerce.",
                'business_finance': "Interest in business/finance strongly suggests Commerce.",
                'creative_expression': "Interest in creative expression points towards Arts/Humanities.",
                'helping_understanding': "Interest in helping/understanding people can lead to Arts/Humanities or people-centric Science fields."
            }
            if activity == 'problem_solving': stream_scores["Science"] += 1.5; stream_scores["Commerce"] += 0.5
            elif activity == 'business_finance': stream_scores["Commerce"] += 1.5; stream_scores["Science"] += 0.2
            elif activity == 'creative_expression': stream_scores["Arts/Humanities"] += 1.5
            elif activity == 'helping_understanding': stream_scores["Arts/Humanities"] += 1.5; stream_scores["Science"] += 0.2
            if activity in activity_reason_map: recommendation_reasoning.append(activity_reason_map[activity])
            
            # 3. Subject Preference
            subject_pref_reason_map = {
                'analytical_logical': "Preference for analytical/logical subjects strengthens Science and some Commerce.",
                'theoretical_memorization': "Preference for theoretical subjects can be found in Arts/Humanities and parts of Science.",
                'practical_application': "Preference for practical application aligns with Commerce and applied Sciences.",
                'language_communication': "Preference for language/communication strongly suggests Arts/Humanities."
            }
            if subject_pref == 'analytical_logical': stream_scores["Science"] += 1.5; stream_scores["Commerce"] += 0.5
            elif subject_pref == 'theoretical_memorization': stream_scores["Arts/Humanities"] += 1.0; stream_scores["Science"] += 0.2
            elif subject_pref == 'practical_application': stream_scores["Commerce"] += 1.0; stream_scores["Science"] += 1.0
            elif subject_pref == 'language_communication': stream_scores["Arts/Humanities"] += 1.5
            if subject_pref in subject_pref_reason_map: recommendation_reasoning.append(subject_pref_reason_map[subject_pref])

            # 4. Quiz Scoring
            quiz_answers_map = {'q1': q1_ans, 'q2': q2_ans, 'q3': q3_ans}
            for q_num_key, ans_key in quiz_answers_map.items():
                if ans_key and ans_key in QUIZ_SCORES.get(q_num_key, {}):
                    scores_for_ans = QUIZ_SCORES[q_num_key][ans_key]
                    stream_scores["Science"] += scores_for_ans.get('S', 0)
                    stream_scores["Commerce"] += scores_for_ans.get('C', 0)
                    stream_scores["Arts/Humanities"] += scores_for_ans.get('A', 0)
            recommendation_reasoning.append("Your quiz answers have also been factored into the scores.")

            # Determine recommended stream type
            recommendation_type = None # Initialize for this POST request
            sorted_streams = sorted(stream_scores.items(), key=lambda item: item[1], reverse=True)
            
            print(f"DEBUG --- Stream Scores Before Final Decision ---")
            print(f"Science Score: {stream_scores.get('Science', 0)}")
            print(f"Commerce Score: {stream_scores.get('Commerce', 0)}")
            print(f"Arts/Humanities Score: {stream_scores.get('Arts/Humanities', 0)}")
            print(f"DEBUG --- Sorted Streams by Score ---: {sorted_streams}")
            
            NO_RECOMMENDATION_THRESHOLD = 2.5 # Example: if highest score is less than this
            SCORE_DIFFERENCE_THRESHOLD = 1.0  # Example: if diff between top 2 is less than this
            print(f"DEBUG --- Thresholds ---: NO_REC_THRESHOLD={NO_RECOMMENDATION_THRESHOLD}, SCORE_DIFF_THRESHOLD={SCORE_DIFFERENCE_THRESHOLD}")


            if not sorted_streams or sorted_streams[0][1] < NO_RECOMMENDATION_THRESHOLD :
                recommendation_type = "NoClearRecommendation"
                recommendation_reasoning.insert(0, "Your responses show a balanced mix of interests or not a strong leaning towards one particular stream. We recommend exploring all streams further or discussing with a career counselor.")
            elif len(sorted_streams) > 1 and (sorted_streams[0][1] - sorted_streams[1][1] < SCORE_DIFFERENCE_THRESHOLD):
                recommendation_type = "MultipleSuggestions"
                primary_rec = sorted_streams[0][0]
                secondary_rec = sorted_streams[1][0]
                recommendation_reasoning.insert(0, f"Your preferences strongly suggest {primary_rec}, with a notable alignment with {secondary_rec}. Explore both!")
                context['primary_recommendation'] = primary_rec
                context['secondary_recommendation'] = secondary_rec
                context['recommended_stream_info_primary'] = STREAM_INFO.get(primary_rec)
                context['recommended_stream_resources_primary'] = STREAM_RESOURCES.get(primary_rec)
                context['recommended_stream_info_secondary'] = STREAM_INFO.get(secondary_rec)
                context['recommended_stream_resources_secondary'] = STREAM_RESOURCES.get(secondary_rec)
                if primary_rec in processed_all_streams: processed_all_streams[primary_rec]['show_in_accordion'] = False
                if secondary_rec in processed_all_streams: processed_all_streams[secondary_rec]['show_in_accordion'] = False
            else:
                recommendation_type = sorted_streams[0][0] 
                if recommendation_type not in SPECIAL_RECOMMENDATION_TYPES:
                     context['recommended_stream_info'] = STREAM_INFO.get(recommendation_type)
                     context['recommended_stream_resources'] = STREAM_RESOURCES.get(recommendation_type)
                     if recommendation_type in processed_all_streams:
                         processed_all_streams[recommendation_type]['show_in_accordion'] = False
                if len(sorted_streams) > 1 and (sorted_streams[0][1] - sorted_streams[1][1] <= 2.5) and sorted_streams[1][0] != recommendation_type : # Check if second is different
                     recommendation_reasoning.append(f"While {recommendation_type} is the primary suggestion, {sorted_streams[1][0]} also showed some alignment based on your responses.")
            
            context['recommendation_type'] = recommendation_type
            context['recommendation_reasoning'] = recommendation_reasoning
            context['all_streams'] = processed_all_streams # Update with modified show_in_accordion flags
        else: 
            print(f"DEBUG: RecommendationInputForm is invalid with errors: {recommendation_form.errors}")
            context['recommendation_type'] = None
            # For invalid form, keep all_streams with 'show_in_accordion': True
            # (which it already is from the GET request part)
            
    print(f"DEBUG: Final context keys for dashboard: {list(context.keys())}")
    return render(request, 'recommender/dashboard.html', context)

# --- College Search Views ---
def college_search_view(request):
    print(f"DEBUG: college_search_view called with GET params: {request.GET}")
    colleges = None
    # Initialize with request.GET to pre-fill the form if parameters are in URL
    form = CollegeSearchForm(request.GET or None) 

    if form.is_valid():
        state = form.cleaned_data.get('state')
        # For city, we get the ID from GET params because JS populates it
        # The form field itself might be City.objects.none() initially
        city_id = request.GET.get('city', None) 
        city_obj = None
        if city_id: 
            try:
                city_obj = City.objects.get(id=int(city_id))
            except (City.DoesNotExist, ValueError, TypeError): # Catch more errors
                print(f"DEBUG (Search): City with id '{city_id}' not found or invalid.")
                pass # city_obj will remain None
        
        stream_tag = form.cleaned_data.get('stream')
        print(f"DEBUG (Search Query Params): State: {state}, City Obj: {city_obj} (from ID: {city_id}), Stream: {stream_tag}")

        query = College.objects.all()
        if state and not city_obj: # If state is selected but no specific city from dropdown
             query = query.filter(city__state=state)
             print(f"DEBUG (Search Filter): By state - {state.name if state else 'None'}")
        if city_obj: # If a specific city is selected via dropdown
            query = query.filter(city=city_obj)
            print(f"DEBUG (Search Filter): By city - {city_obj.name if city_obj else 'None'}")
        if stream_tag:
            query = query.filter(offered_streams=stream_tag)
            print(f"DEBUG (Search Filter): By stream - {stream_tag.name if stream_tag else 'None'}")
        
        colleges = query.order_by('name').distinct()
        print(f"DEBUG (Search Result): Found {colleges.count()} colleges.")
    else:
        if request.GET: # If form was submitted (had GET data) but was invalid
            print(f"DEBUG: CollegeSearchForm is invalid. Errors: {form.errors}")

    context = {
        'form': form,
        'colleges': colleges,
        # 'states': State.objects.all().order_by('name') # Pass states for re-rendering form correctly
    }
    return render(request, 'recommender/college_search_results.html', context)

def load_cities(request):
    state_id = request.GET.get('state_id')
    print(f"DEBUG: load_cities AJAX called for state_id: {state_id}")
    cities_data = []
    if state_id:
        try:
            valid_state_id = int(state_id)
            cities = City.objects.filter(state_id=valid_state_id).order_by('name')
            for city in cities:
                cities_data.append({'id': city.id, 'name': city.name})
        except ValueError:
            print(f"DEBUG: Invalid state_id '{state_id}' for load_cities - not an integer.")
        except State.DoesNotExist: # Should not happen if state_id comes from valid selection
            print(f"DEBUG: State with id '{state_id}' does not exist.")
            
    print(f"DEBUG: Returning cities: {cities_data}")
    return JsonResponse(cities_data, safe=False)