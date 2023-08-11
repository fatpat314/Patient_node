from flask import request
import requests


def register_data(request):
    # This repeats in the CNM
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    password = data['password']
    email = data['email']
    DOB = data['DOB']
    location = data['location']

    url = 'http://localhost:6000/register'
    data = {'first_name': first_name, 'last_name':last_name, 'username': username,'password': password, 'email': email, 'DOB': DOB, 'location': location}
    response = requests.post(url, json=data)
    # print('REGISTER:', response)
    return("hi")

# def location_data(request):
#     data = request.get_json()
#     location = data['location']

#     url = 'http://localhost:6000/location'
#     data = {'location': location}
#     response = request.post(url, json=data)
#     return('hi')