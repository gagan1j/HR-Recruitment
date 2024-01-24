from flask import Flask, render_template, request

app = Flask(__name__)
#postgres://recruitement_process_user:70x3V6yu3EtXN7P72k6WNx8o7xg1b1cK@dpg-cmof330l5elc738sk8qg-a.oregon-postgres.render.com/recruitement_process
# Knowledge Base
knowledge_base = {
    'job_profiles': {
        'software_engineer': {
            'required_skills': ['programming', 'problem-solving', 'communication'],
            'company_culture': 'Innovative and collaborative',
        },
        'data_scientist': {
            'required_skills': ['statistics', 'machine-learning', 'data-analysis'],
            'company_culture': 'Data-driven and analytical',
        },
        'marketing_specialist': {
            'required_skills': ['digital-marketing', 'content-creation', 'social-media'],
            'company_culture': 'Creative and customer-focused',
        },
        # Add more job profiles as needed
    },
    # Add more knowledge base categories as needed
}

# Inference Engine
def evaluate_resume(job_profile, candidate_skills, education, cgpa):
    # Disqualify candidates with CGPA less than 7
    if cgpa < 7:
        return 0  # Match percentage is 0 for disqualified candidates
    
    required_skills = knowledge_base['job_profiles'][job_profile]['required_skills']
    
    # Convert both sets to lowercase for case-insensitive matching
    required_skills_lower = set(skill.lower() for skill in required_skills)
    candidate_skills_lower = set(skill.lower() for skill in candidate_skills)
    
    # Calculate matching skills
    matching_skills = candidate_skills_lower.intersection(required_skills_lower)
    
    # Calculate match percentage based on the ratio of matching skills to total required skills
    match_percentage = (len(matching_skills) / len(required_skills)) * 100
    
    # Additional factors (education and CGPA) can be considered here
    # Normalize CGPA to a percentage scale (assuming CGPA is out of 10)
    cgpa_percentage = (cgpa / 10) * 100
    
    # Ensure that candidates with CGPA >= 8 are considered a strong match
    if cgpa_percentage >= 80:
        match_percentage = max(match_percentage, 70)  # Set match percentage to 70% or higher
    
    return match_percentage


# Explanation Facility
def provide_feedback(match_percentage):
    if match_percentage >= 70:
        return 'This candidate is a strong match for the job.'
    elif match_percentage >= 50:
        return 'This candidate meets some of the job requirements.'
    else:
        return 'This candidate may not be the best fit for the job.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    job_profile = request.form['jobProfile']
    candidate_skills = [skill.strip() for skill in request.form['skills'].split(',')]
    education = request.form['education']
    cgpa = float(request.form['cgpa']) 
    match_percentage = evaluate_resume(job_profile, candidate_skills, education, cgpa)
    feedback = provide_feedback(match_percentage)
    return render_template('index.html', feedback=feedback)

