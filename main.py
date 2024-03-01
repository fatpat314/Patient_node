import config
from dotenv import load_dotenv
# import openai
from flask import Flask, jsonify, request, session, g
from flask_jwt_extended import JWTManager, jwt_required, \
                               create_access_token
from flask_cors import CORS
import requests, names, random, threading, uuid, json
import argparse

from register import register_data
from login import login_data
from profile import profile_data

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY # change this to a random string in production
cloud_url = "http://localhost:8010"
# cloud_url = "https://cognitive-network-manager-rdwl5upzra-uw.a.run.app"
jwt = JWTManager(app)
load_dotenv()

# openai.api_key = config.openai_key

class Patient:
    def __init__(self):
        self.unique_id = str(uuid.uuid4())
        self.dummy_id = self.unique_id[:2]
        self.gender = self._generate_gender()
        self.first_name = names.get_first_name(gender=self.gender)
        self.last_name = names.get_last_name()
        self.username = 'test'
        self.password = f'test{self.dummy_id}'
        self.email = f'test{self.dummy_id}@test.com'
        self.DOB = self._generate_DOB()

    def _generate_gender(self):
        binary = random.choice([0, 1])
        return 'male' if binary == 1 else 'female'

    def _generate_DOB(self):
        return str(random.randint(1922, 2010))

    def display_info(self):
        print("First Name:", self.first_name)
        print("Last Name:", self.last_name)
        print("Gender:", self.gender)
        print("Username:", self.username)
        print("Password:", self.password)
        print("Email:", self.email)
        print("Date of Birth:", self.DOB)

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
        data = "Patient Node"
        return jsonify({'data': data})

@app.route('/register', methods=['POST'])
def register():
    new_patient_id = register_data(request, cloud_url)
    event_url = get_event_server()
    event_url = event_url['url']
    event_url = f'{event_url}/event-patient-register'
    data = {'patient_id': new_patient_id}
    print("event", event_url)
    event_response = requests.post(event_url, json=data)
    return('hi')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_data(request, cloud_url)

@app.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    patient = Patient()
    return profile_data(cloud_url, patient)

def get_event_server():
    event_url = f'{cloud_url}/event_server'
    response = requests.get(event_url)
    return response.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    port = args.port
    app.run(host="0.0.0.0", port=port)
