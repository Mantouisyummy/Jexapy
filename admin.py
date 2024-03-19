import requests
from requests.exceptions import InvalidHeader

from .models import User

class Pterodactyl_Application:
    def __init__(self, base_url, api_key):
        if base_url[-1] == "/":
            base_url = base_url[:-1]
            
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def check(self):
        endpoint = f"{self.base_url}/api/application/users"
        headers = self.headers
        response = requests.get(endpoint, headers=headers)
        if response.ok:
            return True
        else:
            raise InvalidHeader("Invaild APIKey. Did you enter it correctly?")
        
    @property
    def list_uesrs(self) -> User:
        endpoint = f'{self.base_url}/api/application/users'
        headers = self.headers

        response = requests.request('GET', endpoint, headers=headers)
        data = response.json()['data']

        return [User(user) for user in data]

    def create_user(self, username, email, password):
        endpoint = f"{self.base_url}/api/application/users"
        headers = self.headers
        data = {
            "username": username,
            "first_name": username,
            "last_name": username,
            "email": email,
            "password": password
        }
        response = requests.post(endpoint, headers=headers, json=data)
        return response.json()
    
    #server
    
    def suspend_server(self, server: str):
        endpoint = f"{self.base_url}/api/application/servers/{server}/suspend"
        headers = self.headers
        response = requests.post(endpoint, headers=headers)
        
        return response.ok
    
    def unsuspend_server(self, server: str):
        endpoint = f"{self.base_url}/api/application/servers/{server}/unsuspend"
        headers = self.headers
        response = requests.post(endpoint, headers=headers)
        
        return response.ok
    
    def reinstall_server(self, server: str):
        endpoint = f"{self.base_url}/api/application/servers/{server}/reinstall"
        headers = self.headers
        response = requests.post(endpoint, headers=headers)
        
        return response.ok
    
    def delete_server(self, server: str):
        endpoint = f"{self.base_url}/api/application/servers/{server}"
        headers = self.headers
        response = requests.delete(endpoint, headers=headers)
        
        return response.ok