import dataclasses

from requests.exceptions import InvalidHeader

from .admin_models import User, Server, Limits, FeatureLimits, Allocation
from jexapy.utils import request

class Jexactyl_Application:
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

        self.check()

    def check(self):
        endpoint = f"{self.base_url}/api/application/users"
        response = request("GET", endpoint, headers=self.headers)
        if response.ok:
            return True
        else:
            raise InvalidHeader("Invaild APIKey. Did you enter it correctly?")
        
    @property
    def list_uesrs(self) -> User:
        response = request("GET", f'{self.base_url}/api/application/users', headers=self.headers)
        data = response.json()['data']

        return [User(**datalist['attributes']) for datalist in data]

    def create_user(self, username, email, password):
        """
        Creates a new user with the given username, email, and password.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            dict: The JSON response containing information about the created user.

        Raises:
            requests.HTTPError: If the request to create the user fails.

        Note:
            The payload is a dictionary containing the username, first name, last name, email, and password.
        """
        middle_index = len(username) // 2
        payload = {
            "username": username,
            "first_name": username[:middle_index],
            "last_name": username[middle_index:],
            "email": email,
            "password": password
        }
        response = request("POST", f"{self.base_url}/api/application/users", headers=self.headers, payload=payload)
        return response.json()
    
    # server

    @property
    def list_servers(self) -> Server:
        response = request("GET", f"{self.base_url}/api/application/servers/", headers=self.headers)
        data = response.json()['data']

        return [Server(**server['attributes']) for server in data]

    def create_server(self, limits: Limits, feature_limits: FeatureLimits, allocation: int, **kwargs) -> Server:
        """
        Creates a server with the given limits, feature limits, and additional parameters.

        Args:
            limits (Limits): The resource limits for the server.
            feature_limits (FeatureLimits): The feature limits for the server.
            allocation (int): The allocation identifier for the server.
            **kwargs: Additional keyword arguments to pass to the server. 
            The expected keys in kwargs include:
                environment (dict): Environment variables for the server.
                allocation (int): Allocation identifier for the server.
                name (str): Name of the server.
                user (int): User ID for the server owner.
                egg (int): Egg identifier for the server configuration.
                docker_image (str): Docker image to use for the server.
                startup (str): Startup command for the server.

        Returns:
            Server: The created server instance.

        Raises:
            requests.HTTPError: If the request to create the server fails.

        Note:
            The payload is a dictionary containing the limits, feature limits, allocation, and additional parameters.
            The additional keyword arguments are included in the payload and must be JSON serializable.
        """
        limits_dict = dataclasses.asdict(limits)
        feature_limits_dict = dataclasses.asdict(feature_limits)

        payload = {
            "limits": limits_dict,
            "feature_limits": feature_limits_dict,
            "allocation": {"default": allocation},
            **kwargs
        }

        response = request("POST", f"{self.base_url}/api/application/servers", headers=self.headers, payload=payload)
        return Server(**response.json()['attributes'])

    def update_server(self, server: str, name: str, user: int, external_id: str, description: str, renewable: bool, renewal: int) -> bool:
        """
        Updates the details of a server.

        Args:
            server (str): The ID of the server to update.
            name (str): The new name for the server.
            user (int): The ID of the user associated with the server.
            external_id (str): The new external ID for the server.
            description (str): The new description for the server.
            renewable (bool): Whether the server is renewable.
            renewal (int): The renewal period for the server.

        Returns:
            bool: True if the server was successfully updated, False otherwise.
        """
        payload = {
            "name": name,
            "user": user,
            "external_id": external_id,
            "description": description,
            "renewable": renewable,
            "renewal": renewal
        }
        response = request("PATCH", f"{self.base_url}/api/application/servers/{server}/details", headers=self.headers, payload=payload)
        return response.ok

    def get_server(self, server: str) -> Server:
        response = request("GET", f"{self.base_url}/api/application/servers/{server}", headers=self.headers)
        return Server(**response.json()['attributes'])

    def suspend_server(self, server: str) -> bool:
        response = request("POST", f"{self.base_url}/api/application/servers/{server}/suspend", headers=self.headers)
        return response.ok
    
    def unsuspend_server(self, server: str) -> bool:
        response = request("POST",f"{self.base_url}/api/application/servers/{server}/unsuspend", headers=self.headers)
        return response.ok
    
    def reinstall_server(self, server: str) -> bool:
        response = request("POST", f"{self.base_url}/api/application/servers/{server}/reinstall", headers=self.headers)
        return response.ok
    
    def delete_server(self, server: str) -> bool:
        response = request("DELETE", f"{self.base_url}/api/application/servers/{server}", headers=self.headers)
        return response.ok

    # Node
    @property
    def list_nodes(self, node: int) -> list[Allocation]:
        """
        Retrieves a list of allocations for a specific node.

        Args:
            node (int): The ID of the node for which to retrieve allocations.

        Returns:
            list[Allocation]: A list of Allocation objects representing the allocations for the specified node.
        """
        response = request("GET", f"{self.base_url}/api/application/nodes/{node}/allocations", headers=self.headers)
        data = response.json()['data']

        return [Allocation(**server['attributes']) for server in data]