import requests
from requests.exceptions import InvalidHeader

from .admin_models import User, Server

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

        response = requests.get(endpoint, headers=headers)
        data = response.json()['data']

        return [User(**datalist['attributes']) for datalist in data]

    def create_user(self, username, email, password):
        endpoint = f"{self.base_url}/api/application/users"
        headers = self.headers
        middle_index = len(username) // 2
        payload = {
            "username": username,
            "first_name": username[:middle_index],
            "last_name": username[middle_index:],
            "email": email,
            "password": password
        }
        response = requests.post(endpoint, headers=headers, json=payload)
        return response.json()
    
    #server

    @property
    def list_servers(self) -> Server:
        endpoint = f"{self.base_url}/api/application/servers/"
        headers = self.headers
        response = requests.get(endpoint, headers=headers)
        data = response.json()['data']

        return [Server(**server['attributes']) for server in data]
    
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