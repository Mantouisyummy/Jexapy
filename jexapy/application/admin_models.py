from dataclasses import dataclass, fields
from typing import Optional
from datetime import datetime

from jexapy.utils import create_environment_dataclass

@dataclass
class Limits:
    """
    The limits of the server

    """
    memory: int
    swap: int
    disk: int
    io: int
    cpu: int
    threads: Optional[int]

    @classmethod
    def from_dict(cls, limits_dict):
        field_names = [field.name for field in fields(cls)]
        kwargs = {field: limits_dict.get(field) for field in field_names}
        return cls(**kwargs)

@dataclass
class FeatureLimits:
    databases: int
    allocations: int
    backups: int

    @classmethod
    def from_dict(cls, feature_dict):
        field_names = [field.name for field in fields(cls)]
        kwargs = {field: feature_dict.get(field) for field in field_names}
        return cls(**kwargs)

@dataclass
class Container:
    startup_command: str
    image: str
    installed: bool
    environment: dict

    @classmethod
    def from_dict(cls, container_dict):
        field_names = [field.name for field in fields(cls)]
        kwargs = {field: container_dict.get(field) for field in field_names}
        return cls(**kwargs)
    
    def __post_init__(self):
        self.environment = create_environment_dataclass(self.environment)

@dataclass
class Server:
    id: int
    external_id: str
    uuid: str
    identifier: str
    name: str
    description: str
    suspended: bool
    limits: Limits
    feature_limits: FeatureLimits
    user: int
    node: int
    allocation: int
    nest: int
    egg: int
    status: str
    container: Container
    updated_at: str
    created_at: str

    def __post_init__(self):
        self.feature_limits = FeatureLimits.from_dict(self.feature_limits)
        self.container = Container.from_dict(self.container)


@dataclass
class User:
    id: int
    external_id: str
    uuid: str
    username: str
    email: str
    first_name: str
    last_name: str
    language: str
    root_admin: bool
    twofa: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class Allocation:
    id: int
    ip: str
    ailas: Optional[str]
    port: int
    notes: Optional[str]
    assigned: bool
