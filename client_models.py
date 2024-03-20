from dataclasses import dataclass, field

from typing import List

@dataclass
class User:
    id: int
    admin: bool
    username: str
    email: str
    first_name: str
    last_name: str
    language: str

@dataclass
class SftpDetails:
    ip: str
    port: int

@dataclass
class Limit:
    memory: int
    swap: int
    disk: int
    io: int
    cpu: int

@dataclass
class FeatureLimits:
    databases: int
    allocations: int
    backups: int

@dataclass
class Allocation:
    id: int
    ip: str
    ip_alias: str
    port: int
    notes: str
    is_default: bool

@dataclass
class Server:
    server_owner: bool
    identifier: str
    uuid: str
    name: str
    node: str
    sftp_details: SftpDetails
    description: str
    limits: Limit
    feature_limits: FeatureLimits
    is_suspended: bool
    is_installing: bool
    relationships: dict
    allocations: List[Allocation] = field(default_factory=list)