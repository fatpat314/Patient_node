from flask import request
import requests


def register_data(request, cloud_url):
    # This repeats in the CNM
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    password = data['password']
    email = data['email']
    DOB = data['DOB']
    location = data['location']

    url = f'{cloud_url}/register'
    data = {'first_name': first_name, 'last_name':last_name, 'username': username,'password': password, 'email': email, 'DOB': DOB, 'location': location}
    response = requests.post(url, json=data)
    print('REGISTER:', response.json())
    return(response.json())

# def location_data(request):
#     data = request.get_json()
#     location = data['location']

#     url = 'http://localhost:6000/location'
#     data = {'location': location}
#     response = request.post(url, json=data)
#     return('hi')