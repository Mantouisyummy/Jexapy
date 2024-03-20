import requests
import json
import urllib.parse

from .exceptions import AuthFailed
from .client_models import Server, User

class Pterodactyl_Client:
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
        endpoint = f"{self.base_url}/api/client/account"
        headers = self.headers
        response = requests.get(endpoint, headers=headers)
        if response.ok:
            return True
        else:
            raise AuthFailed("Invaild APIKey. Did you enter it correctly?")

        
    @property
    def list_servers(self):
        endpoint = f'{self.base_url}/api/client'
        headers = self.headers

        response = requests.request('GET', endpoint, headers=headers)
        data = response.json()['data']

        return [Server(server['attributes']) for server in data]
        
    @property
    def account_details(self) -> User:
        endpoint = f'{self.base_url}/api/client/account'
        headers = self.headers

        response = requests.request('GET', endpoint, headers=headers)
        return User(response.json()['attributes'])

    def details_2FA(self):
        endpoint = f'{self.base_url}/api/client/account/two-factor'
        headers = self.headers

        response = requests.request('GET', endpoint, headers=headers)
        return response.json()

    def enable_2FA(self, code):
        endpoint = f'{self.base_url}/api/client/account/two-factor'
        headers = self.headers
        payload = {"code": code}

        response = requests.request(
            'POST', endpoint, data=json.dumps(payload), headers=headers)
        return response.json()

    def disable_2FA(self, password):
        endpoint = f'{self.base_url}/api/client/account/two-factor'
        headers = self.headers
        payload = {"password": password}

        response = requests.request(
            'DELETE', endpoint, data=json.dumps(payload), headers=headers)
        return response

    def update_email(self, email, password):
        endpoint = f'{self.base_url}/api/client/account/email'
        headers = self.headers
        payload = {"email": email, "password": password}

        response = requests.request(
            'PUT', endpoint, data=json.dumps(payload), headers=headers)
        return response

    def update_password(self, current_password, new_password):
        endpoint = f'{self.base_url}/api/client/account/password'
        headers = self.headers
        payload = {"current_password": current_password,
                   "password": new_password, "password_confirmation": new_password}
        response = requests.request(
            'PUT', endpoint, data=json.dumps(payload), headers=headers)
        return response
    
    @property
    def list_API_keys(self):
        endpoint = f'{self.base_url}/api/client/account/api-keys'
        headers = self.headers

        response = requests.request('GET', endpoint, headers=headers)
        return response.json()

    def create_API_key(self, description, allowed_ips: list = None):
        endpoint = f'{self.base_url}/api/client/account/api-keys'
        headers = self.headers
        if allowed_ips == None:
            payload = {"description": description}
        else:
            payload = {"description": description, "allowed_ips": allowed_ips}

        response = requests.request(
            'POST', endpoint, data=json.dumps(payload), headers=headers)
        return response.json()

    def delete_API_key(self, key_identifier):
        endpoint = f'{self.base_url}/api/client/account/api-keys/{key_identifier}'
        headers = self.headers
        response = requests.request('DELETE', endpoint,  headers=headers)
        return response

    def list_databases(self, server):
        endpoint = f'{self.base_url}/api/client/servers/{server}/databases'
        headers = self.headers
        response = requests.request('GET', endpoint,  headers=headers)
        return response.json()

    def create_databases(self, server, database, remote):
        endpoint = f'{self.base_url}/api/client/servers/{server}/databases'
        headers = self.headers
        payload = {
            "database": database,
            "remote": remote
        }
        response = requests.request(
            'POST', endpoint, data=json.dumps(payload), headers=headers)
        return response.json()

    def rotate_password(self, database):
        endpoint = f'{self.base_url}/api/client/servers/1a7ce997/databases/{database}/rotate-password'
        headers = self.headers
        response = requests.request('POST', endpoint, headers=headers)
        return response.json()

    def delete_database(self, server, database):
        endpoint = f'{self.base_url}/api/client/servers/{server}/databases/{database}'
        headers = self.headers
        response = requests.request('DELETE', endpoint, headers=headers)
        return response

    def list_files(self, server, directory=None):
        if directory:
            endpoint = f'{self.base_url}/api/client/servers/{server}/files/list?directory={urllib.parse.quote_plus(directory)}'
        else:
            endpoint = f'{self.base_url}/api/client/servers/{server}/files/list'
        headers = self.headers
        response = requests.request('GET', endpoint, headers=headers)
        return response.json()

    def get_file_contents(self, server, file):
        endpoint = f'{self.base_url}/api/client/servers/{server}/files/contents?file={urllib.parse.quote_plus(file)}'
        headers = self.headers
        response = requests.request('GET', endpoint,  headers=headers)
        return response.text

    def download_file(self, server, file):
        endpoint = f'{self.base_url}/api/client/servers/{server}/files/download?file={urllib.parse.quote_plus(file)}'
        headers = self.headers
        response = requests.request('GET', endpoint, headers=headers)
        return response.json()['attributes']['url']

    def rename_file(self, server,root,files):
        endpoint = f'{self.base_url}/api/client/servers/{server}/files/rename'
        headers = self.headers
        payload = {
            "root": root,
            "files":files
        }

        response = requests.request('PUT', endpoint, data=json.dumps(payload), headers=headers)
        return response

   
    def server_details(self, server: int) -> Server:
        endpoint = f"{self.base_url}/api/client/servers/{server}"
        headers = self.headers
        
        response = requests.request('GET', endpoint, headers=headers)
        print(response.status_code)
        return Server(response.json())

    def stop_server(self, server: str):
        endpoint = f'{self.base_url}/api/client/servers/{server}/power'
        headers = self.headers
        payload = '{"signal": "stop"}'

        response = requests.request('POST', endpoint, data=payload, headers=headers)
        return response

    def start_server(self, server: str):
        endpoint = f'{self.base_url}/api/client/servers/{server}/power'
        headers = self.headers
        payload = '{"signal": "start"}'

        response = requests.request('POST', endpoint, data=payload, headers=headers)
        return response

    def restart_server(self, server: str):
        endpoint = f'{self.base_url}/api/client/servers/{server}/power'
        headers = self.headers
        payload = '{"signal": "restart"}'

        response = requests.request('POST', endpoint, data=payload, headers=headers)
        return response

    def kill_server(self, server: str):
        endpoint = f'{self.base_url}/api/client/servers/{server}/power'
        headers = self.headers
        payload = '{"signal": "kill"}'

        response = requests.request('POST', endpoint, data=payload, headers=headers)
        return response

    def rename_server(self, server: str, name: str):
        endpoint = f'{self.base_url}/api/client/servers/{server}/settings/rename'
        headers = self.headers
        payload = {"name": name}
        response = requests.request(
            'POST', endpoint, data=json.dumps(payload), headers=headers)
        return response

    def send_command(self, server: str, command: str):
        endpoint = f'{self.base_url}/api/client/servers/{server}/command'
        headers = self.headers
        payload = {"command": command}
        response = requests.request(
            'POST', endpoint, data=json.dumps(payload), headers=headers)
        return response