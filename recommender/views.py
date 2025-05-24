# File: career_guidance_system/recommender/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse # Keep for potential future debugging
# JsonResponse is NOT needed as load_cities is removed
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# CollegeSearchForm is removed from this import
from .forms import CustomUserCreationForm, RecommendationInputForm
# College, City, State, StreamTag models are removed from this import (ensure they are removed from models.py too)
# from .models import College, City, State, StreamTag 

# --- Stream Data ---
STREAM_INFO = {
    "Science": {
        "description": "Focuses on Physics, Chemistry, Mathematics/Biology. Prepares for engineering, medical, research fields, and a wide array of specialized technical and analytical roles.",
        "benefits": ["Develops strong analytical, problem-solving, and quantitative skills.","Wide range of higher education options (Engineering, Medical, BSc, etc.).","Foundation for research and innovation."],
        "opportunities": [
            "Engineer (Software, Mechanical, Civil, Electrical, Chemical, Aerospace, etc.)", "Doctor (MBBS, BDS, BAMS, BHMS, etc.)", "Pharmacist", "Architect", "Pilot",
            "Research Scientist (Physics, Chemistry, Biology, Math, etc.)", "Data Scientist / Analyst (often requires strong math/stats)", "Biomedical Engineer", "Genetic Counselor",
            "Food Scientist / Technologist", "Forensic Scientist", "Marine Biologist / Oceanographer", "Environmental Scientist / Consultant", "Geologist / Geophysicist",
            "Meteorologist / Climatologist", "Astrophysicist / Astronomer", "Actuary (requires strong math & statistics)", "Robotics Engineer", "Nanotechnologist",
            "Bioinformatician", "Epidemiologist", "Patent Lawyer (with a science/engineering degree + law degree)", "Scientific Writer / Medical Writer",
            "GIS (Geographic Information Systems) Specialist", "UX Researcher (often blends psychology with tech understanding)", "Clinical Research Coordinator", "Medical Physicist"
        ],
        "salary_expectation": "Varies widely. Entry-level for core engineering/medical roles can be moderate to high, growing significantly with experience. Specialized and niche roles can also offer very competitive salaries, often depending on demand, expertise, and further qualifications. Research salaries depend on funding and field."
    },
    "Commerce": {
        "description": "Focuses on Accountancy, Business Studies, Economics, and Mathematics. Prepares for careers in finance, business operations, management, and specialized commercial roles.",
        "benefits": ["Develops understanding of business operations, financial systems, and economic principles.","Excellent for aspiring entrepreneurs, managers, and financial professionals.","Wide range of professional certifications (CA, CS, CFA) and degree options (B.Com, BBA, MBA, M.Com, Economics Hons)."],
        "opportunities": [
            "Chartered Accountant (CA)", "Company Secretary (CS)", "Banker (Retail, Corporate)", "Financial Analyst", "Business Manager / Operations Manager",
            "Marketing Manager / Sales Manager", "Human Resources Manager", "Economist", "Investment Banker", "Actuary (also linked with Science)",
            "Forensic Accountant", "Management Consultant (various specializations like Strategy, IT, HR)", "Supply Chain Manager / Logistics Specialist",
            "Risk Manager / Analyst", "Business Valuator", "Stockbroker / Equity Research Analyst", "Digital Marketing Specialist / SEO/SEM Expert",
            "E-commerce Manager", "International Business Consultant", "Cost and Management Accountant (CMA)", "Certified Financial Planner (CFP)",
            "Auditor (Internal/External)", "Business Data Analyst (overlaps with Science)"
        ],
        "salary_expectation": "Good potential. Professional certifications like CA, CS, CFA, and MBAs from top schools often lead to high earning potential. Roles in investment banking, consulting, and specialized finance can be very lucrative."
    },
    "Arts/Humanities": {
        "description": "Focuses on subjects like History, Political Science, Languages, Literature, Psychology, Sociology, Fine Arts, etc. Prepares for diverse fields including civil services, law, journalism, education, creative industries, and social work.",
        "benefits": ["Develops strong critical thinking, communication, writing, and creative skills.","Provides a broad understanding of society, culture, and human behavior.","Offers diverse pathways to careers in public service, media, education, law, and the arts."],
        "opportunities": [
            "Lawyer / Advocate", "Journalist / Reporter / Editor", "Teacher / Professor (School, College)", "Psychologist (Clinical, Counselling, Organizational)",
            "Graphic Designer / Web Designer", "Content Writer / Copywriter", "Civil Servant (IAS, IPS, IFS, etc.)", "Archaeologist / Historian / Archivist",
            "Museum Curator / Art Conservator", "Librarian / Information Scientist", "Urban and Regional Planner", "Sociologist / Anthropologist",
            "Political Analyst / Psephologist", "Public Relations Specialist", "Social Media Manager / Digital Content Creator", "Scriptwriter (Film, TV, Web)",
            "Technical Writer", "Translator / Interpreter", "Foreign Language Expert (Diplomacy, Corporate)", "Event Manager", "Fashion Designer / Stylist",
            "Interior Designer", "Animator / Multimedia Artist", "Art Therapist / Music Therapist / Drama Therapist", "Social Worker / NGO Coordinator",
            "Policy Analyst / Researcher (Social Sector)", "UX Writer / Content Strategist"
        ],
        "salary_expectation": "Highly variable. Top lawyers, successful civil servants, and established professionals in media/design can earn very well. Many roles offer immense job satisfaction and opportunities for societal impact. Salaries in some creative or social sectors might start lower but can grow with experience and reputation."
    }
}
# --- END Stream Data --- #

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
# --- END Resource Data --- #

# --- Quiz Scoring Data ---
QUIZ_SCORES = {
    'q1': { 'q1_a': {'S': 2,   'C': 1,   'A': 0}, 'q1_b': {'S': 0.5, 'C': 2,   'A': 1}, 'q1_c': {'S': 0,   'C': 0.5, 'A': 2}, 'q1_d': {'S': 0,   'C': 1,   'A': 1.5},},
    'q2': { 'q2_a': {'S': 2,   'C': 0.5, 'A': 0}, 'q2_b': {'S': 0,   'C': 2,   'A': 0.5}, 'q2_c': {'S': 0,   'C': 0.5, 'A': 2}, 'q2_d': {'S': 1,   'C': 1,   'A': 1.5},},
    'q3': { 'q3_a': {'S': 2,   'C': 0.5, 'A': 0}, 'q3_b': {'S': 0,   'C': 2,   'A': 0.5}, 'q3_c': {'S': 0,   'C': 0,   'A': 2}, 'q3_d': {'S': 1,   'C': 0.5, 'A': 1.5},}
}
# --- END Quiz Scoring --- #

# --- Entrance Exam Data ---
STREAM_ENTRANCE_EXAMS = {
    "Science": [
        {"name": "JEE Main & Advanced", "for_courses": "B.E./B.Tech (Engineering)", "eligibility": "10+2 with PCM", "website": "https://jeemain.nta.nic.in/", "typical_period": "Jan & Apr"},
        {"name": "NEET (UG)", "for_courses": "MBBS, BDS, AYUSH courses", "eligibility": "10+2 with PCB", "website": "https://neet.nta.nic.in/", "typical_period": "May"},
        {"name": "NATA / JEE Main (Paper 2)", "for_courses": "B.Arch (Architecture)", "eligibility": "10+2 with PCM or 10+3 Diploma", "website": "https://www.nata.in/", "typical_period": "Varies"},
        {"name": "ICAR AIEEA", "for_courses": "B.Sc. Agriculture & allied", "eligibility": "10+2 Science", "website": "https://icar.nta.nic.in/", "typical_period": "June/July"},
    ],
    "Commerce": [
        {"name": "CLAT", "for_courses": "Integrated LLB (5 years)", "eligibility": "10+2 (any stream)", "website": "https://consortiumofnlus.ac.in/", "typical_period": "December"},
        {"name": "CA Foundation", "for_courses": "Chartered Accountancy", "eligibility": "Passed 10+2", "website": "https://www.icai.org/", "typical_period": "May/June & Nov/Dec"},
        {"name": "CSEET", "for_courses": "Company Secretary", "eligibility": "10+2", "website": "https://www.icsi.edu/", "typical_period": "Multiple"},
    ],
    "Arts/Humanities": [
        {"name": "CLAT", "for_courses": "Integrated LLB (5 years)", "eligibility": "10+2 (any stream)", "website": "https://consortiumofnlus.ac.in/", "typical_period": "December"},
        {"name": "NID DAT / UCEED", "for_courses": "Design (B.Des)", "eligibility": "10+2 (any stream)", "website": "http://admissions.nid.edu/", "typical_period": "Jan/Feb"},
        {"name": "NCHM JEE", "for_courses": "B.Sc. Hospitality", "eligibility": "10+2", "website": "https://nchmjee.nta.nic.in/", "typical_period": "May"},
    ]
}
# --- END Entrance Exam Data --- #

# --- Financial Aid Data ---
FINANCIAL_AID_INFO = {
    "Scholarships": [
        {"name": "National Scholarship Portal (NSP)", "url": "https://scholarships.gov.in/", "description": "Govt. scholarships (merit, means, category-based)."},
        {"name": "State Scholarship Portals", "url": "#", "description": "Check your respective state's portal."},
    ],
    "Education Loans": [
        {"name": "Vidya Lakshmi Portal", "url": "https://www.vidyalakshmi.co.in/", "description": "Govt. portal for education loan applications."},
        {"name": "Bank Education Loans", "url": "#", "description": "Most banks offer education loans. Compare terms."},
    ],
    "Important Note": [
        {"name": "Verify Eligibility & Deadlines", "url": "#", "description": "Always check official websites for current details."},
    ]
}
# --- END Financial Aid Data --- #


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
            print(f"DEBUG: Registration form is invalid with errors: {form.errors}")
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
    # college_search_form is REMOVED

    # Initialize context with all necessary data for GET requests
    # Make a copy of STREAM_INFO to modify 'show_in_accordion' without affecting the global constant.
    processed_all_streams = {key: data.copy() for key, data in STREAM_INFO.items()}
    for stream_data_val in processed_all_streams.values():
        stream_data_val['show_in_accordion'] = True # Default to show

    context = {
        'form': recommendation_form,             
        # 'college_search_form': None, # REMOVED from context
        'STREAM_RESOURCES': STREAM_RESOURCES,
        'all_streams': processed_all_streams, 
        'SPECIAL_RECOMMENDATION_TYPES': SPECIAL_RECOMMENDATION_TYPES,
        'recommendation_type': None, 
        'recommendation_reasoning': [],
        'STREAM_ENTRANCE_EXAMS': STREAM_ENTRANCE_EXAMS, 
        'FINANCIAL_AID_INFO': FINANCIAL_AID_INFO,       
        # Initialize keys that will be set in POST if a recommendation is made
        'relevant_entrance_exams': None,
        'relevant_entrance_exams_primary': None,
        'relevant_entrance_exams_secondary': None,
        'primary_recommendation': None,
        'secondary_recommendation': None,
        'recommended_stream_info_primary': None,
        'recommended_stream_resources_primary': None,
        'recommended_stream_info_secondary': None,
        'recommended_stream_resources_secondary': None,
        'recommended_stream_info': None,
        'recommended_stream_resources': None,
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
            # recommendation_reasoning must be actively managed in context
            context['recommendation_reasoning'] = [] # Reset for new recommendation

            # 1. Percentage-based
            base_recommendation_perc = ""
            if percentage >= 85: stream_scores["Science"] += 2.5; base_recommendation_perc = "Science (strong)"
            elif percentage >= 75: stream_scores["Science"] += 1.5; stream_scores["Commerce"] += 1.0; base_recommendation_perc = "Science or Commerce"
            elif percentage >= 60: stream_scores["Commerce"] += 1.5; stream_scores["Science"] += 0.5; stream_scores["Arts/Humanities"] += 0.5; base_recommendation_perc = "Commerce or Arts/Science"
            elif percentage >= 45: stream_scores["Arts/Humanities"] += 1.5; stream_scores["Commerce"] += 0.5; base_recommendation_perc = "Arts or Commerce"
            else: stream_scores["Arts/Humanities"] += 2.5; base_recommendation_perc = "Arts/Humanities (strong)"
            if percentage > 0 : context['recommendation_reasoning'].append(f"Your percentage ({percentage}%) suggests: {base_recommendation_perc}.")

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
            if activity in activity_reason_map: context['recommendation_reasoning'].append(activity_reason_map[activity])
            
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
            if subject_pref in subject_pref_reason_map: context['recommendation_reasoning'].append(subject_pref_reason_map[subject_pref])

            # 4. Quiz Scoring
            quiz_answers_map = {'q1': q1_ans, 'q2': q2_ans, 'q3': q3_ans}
            for q_num_key, ans_key in quiz_answers_map.items():
                if ans_key and ans_key in QUIZ_SCORES.get(q_num_key, {}):
                    scores_for_ans = QUIZ_SCORES[q_num_key][ans_key]
                    stream_scores["Science"] += scores_for_ans.get('S', 0)
                    stream_scores["Commerce"] += scores_for_ans.get('C', 0)
                    stream_scores["Arts/Humanities"] += scores_for_ans.get('A', 0)
            context['recommendation_reasoning'].append("Your quiz answers have also been factored into the scores.")

            # Determine recommended stream type
            recommendation_type = None 
            sorted_streams = sorted(stream_scores.items(), key=lambda item: item[1], reverse=True)
            
            print(f"DEBUG --- Stream Scores Before Final Decision ---")
            print(f"Science Score: {stream_scores.get('Science', 0)}")
            print(f"Commerce Score: {stream_scores.get('Commerce', 0)}")
            print(f"Arts/Humanities Score: {stream_scores.get('Arts/Humanities', 0)}")
            print(f"DEBUG --- Sorted Streams by Score ---: {sorted_streams}")
            
            NO_RECOMMENDATION_THRESHOLD = 2.5 
            SCORE_DIFFERENCE_THRESHOLD = 1.0  
            print(f"DEBUG --- Thresholds ---: NO_REC_THRESHOLD={NO_RECOMMENDATION_THRESHOLD}, SCORE_DIFF_THRESHOLD={SCORE_DIFFERENCE_THRESHOLD}")

            if not sorted_streams or sorted_streams[0][1] < NO_RECOMMENDATION_THRESHOLD :
                recommendation_type = "NoClearRecommendation"
                context['recommendation_reasoning'].insert(0, "Your responses show a balanced mix of interests or not a strong leaning towards one particular stream. We recommend exploring all streams further or discussing with a career counselor.")
            elif len(sorted_streams) > 1 and (sorted_streams[0][1] - sorted_streams[1][1] < SCORE_DIFFERENCE_THRESHOLD):
                recommendation_type = "MultipleSuggestions"
                primary_rec = sorted_streams[0][0]
                secondary_rec = sorted_streams[1][0]
                context['recommendation_reasoning'].insert(0, f"Your preferences strongly suggest {primary_rec}, with a notable alignment with {secondary_rec}. Explore both!")
                context['primary_recommendation'] = primary_rec
                context['secondary_recommendation'] = secondary_rec
                context['recommended_stream_info_primary'] = STREAM_INFO.get(primary_rec)
                context['recommended_stream_resources_primary'] = STREAM_RESOURCES.get(primary_rec)
                context['recommended_stream_info_secondary'] = STREAM_INFO.get(secondary_rec)
                context['recommended_stream_resources_secondary'] = STREAM_RESOURCES.get(secondary_rec)
                if primary_rec in processed_all_streams: processed_all_streams[primary_rec]['show_in_accordion'] = False
                if secondary_rec in processed_all_streams: processed_all_streams[secondary_rec]['show_in_accordion'] = False
                context['relevant_entrance_exams_primary'] = STREAM_ENTRANCE_EXAMS.get(primary_rec, [])
                context['relevant_entrance_exams_secondary'] = STREAM_ENTRANCE_EXAMS.get(secondary_rec, [])
            else:
                recommendation_type = sorted_streams[0][0] 
                if recommendation_type not in SPECIAL_RECOMMENDATION_TYPES:
                     context['recommended_stream_info'] = STREAM_INFO.get(recommendation_type)
                     context['recommended_stream_resources'] = STREAM_RESOURCES.get(recommendation_type)
                     context['relevant_entrance_exams'] = STREAM_ENTRANCE_EXAMS.get(recommendation_type, [])
                     if recommendation_type in processed_all_streams:
                         processed_all_streams[recommendation_type]['show_in_accordion'] = False
                if len(sorted_streams) > 1 and (sorted_streams[0][1] - sorted_streams[1][1] <= 2.5) and sorted_streams[1][0] != recommendation_type : 
                     context['recommendation_reasoning'].append(f"While {recommendation_type} is the primary suggestion, {sorted_streams[1][0]} also showed some alignment based on your responses.")
            
            context['recommendation_type'] = recommendation_type
            # 'recommendation_reasoning' is already updated in the context through context['recommendation_reasoning'].append(...)
            context['all_streams'] = processed_all_streams 
        else: 
            print(f"DEBUG: RecommendationInputForm is invalid with errors: {recommendation_form.errors}")
            context['recommendation_type'] = None
            context['recommendation_reasoning'] = [] # Clear reasoning if form is invalid
            
    # Debug prints for context, just before rendering
    print(f"DEBUG: Final context keys for dashboard: {list(context.keys())}")
    if 'recommendation_type' in context:
        print(f"DEBUG CONTEXT: recommendation_type = {context.get('recommendation_type')}")
    else:
        print("DEBUG CONTEXT: recommendation_type is NOT in context")
    
    print(f"DEBUG CONTEXT: FINANCIAL_AID_INFO (exists?) = {'FINANCIAL_AID_INFO' in context and bool(context.get('FINANCIAL_AID_INFO'))}")
    print(f"DEBUG CONTEXT: STREAM_ENTRANCE_EXAMS (exists?) = {'STREAM_ENTRANCE_EXAMS' in context and bool(context.get('STREAM_ENTRANCE_EXAMS'))}")
    print(f"DEBUG CONTEXT: relevant_entrance_exams = {context.get('relevant_entrance_exams')}")
    print(f"DEBUG CONTEXT: relevant_entrance_exams_primary = {context.get('relevant_entrance_exams_primary')}")
    print(f"DEBUG CONTEXT: relevant_entrance_exams_secondary = {context.get('relevant_entrance_exams_secondary')}")
        
    return render(request, 'recommender/dashboard.html', context)

# --- REMOVED College Search Views (college_search_view, load_cities) ---