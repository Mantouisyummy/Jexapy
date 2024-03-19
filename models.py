from datetime import datetime

from .exceptions import NoDataException

class Server:
    def __init__(self, data: dict):
        self._data: str = data.get('data', None)
        if self._data is None:
            raise NoDataException("Data not found. Are you sure you're entering the correct identifier?")
        
        attributes: dict = self._data.get('attributes')
        limits: dict = attributes.get('limits')
        
        self.identifier: int = attributes['identifier']
        self.name: str = attributes['name']
        self.description: str = attributes['description']
        self.node: str = attributes['node']
        self.image = attributes['docker_image']
        self.cpu: int = limits['cpu']
        self.memory: int = limits['memory']
        self.disk: int = limits['disk']
        self.is_suspended: bool = attributes['is_suspended']
    
    
    def __repr__(self) -> str:
        return '<Server name={0.name} description={0.description} identifier={0.identifier} node={0.node} image={0.image} cpu={0.cpu} memory={0.memory} desk={0.disk} is_suspended={0.is_suspended}>'.format(self)
        
class User:
    def __init__(self, data: dict):
        self._data: str = data.get('data', None)
        if self._data is None:
            raise NoDataException("Data not found. Are you sure you're entering the correct identifier?")
        
        attributes: dict = self._data.get('attributes')
        self.id: int = attributes['id']
        self.username: str = attributes['username']
        self.created_at: datetime = attributes.get('created_at', None)
        self.admin: bool = attributes['root_admin']
    
    def __repr__(self) -> str:
        return '<User username={0.username} id={0.id} created_at={0.created_at} admin={0.admin}>'.format(self)