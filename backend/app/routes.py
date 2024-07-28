from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_from_directory, flash
from .ai_assistant import AI_Assistant

main = Blueprint('main', __name__)

ai_assistant = AI_Assistant()

@main.route('/')
def index():
    return render_template('main.html')

@main.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if verify_user(email, password):  
            return redirect(url_for('main.form'))
        else:
            flash('Invalid email or password')
    return render_template('signin.html')

@main.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        process_answers(answer1, answer2) 
        return redirect(url_for('main.thanks'))
    return render_template('form.html')

@main.route('/ai')
def ai():
    return render_template('Ai.html')

@main.route('/interviewer')
def interviewer():
    return render_template('interviewer.html')

@main.route('/thanks')
def thanks():
    return render_template('thanks.html')

@main.route('/process_ai', methods=['POST'])
def process_ai():
    data = request.json
    question = data.get('question')
    
    # Get the AI response
    ai_response = ai_assistant.generate_ai_response(question)
    
    return jsonify({'response': ai_response})

@main.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('../static', filename)

def verify_user(email, password):
    # Implement user verification logic here
    # Example: check against database
    return True

def process_answers(answer1, answer2):
    # Implement answer processing logic here
    # Example: save to database or send to AI model for analysis
    pass

def ai_interview_response(question):
    response = ai_assistant.generate_ai_response(question)
    return response
