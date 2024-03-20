from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Limits:
    memory: int
    swap: int
    disk: int
    io: int
    cpu: int
    threads: Optional[int]

@dataclass
class FeatureLimits:
    databases: int
    allocations: int
    backups: int

@dataclass
class Environment:
    SERVER_JARFILE: str
    VANILLA_VERSION: str
    STARTUP: str
    P_SERVER_LOCATION: str
    P_SERVER_UUID: str
    P_SERVER_ALLOCATION_LIMIT: int

@dataclass
class Container:
    startup_command: str
    image: str
    installed: bool
    environment: Environment

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
    pack: Optional[str]
    container: Container
    updated_at: str
    created_at: str

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