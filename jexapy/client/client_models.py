from dataclasses import dataclass, field, fields

from typing import List, Any, Optional

import requests

@dataclass
class User:
    id: int
    admin: bool
    username: str
    email: str
    first_name: str
    last_name: str
    language: str
    money: int
        
@dataclass
class SftpDetails:
    ip: str
    port: int

    @classmethod
    def from_dict(cls, limits_dict):
        field_names = [field.name for field in fields(cls)]
        kwargs = {field: limits_dict.get(field) for field in field_names}
        return cls(**kwargs)

@dataclass
class Limits:
    memory: int
    swap: int
    disk: int
    io: int
    cpu: int
    threads: str
    oom_disabled: bool

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
class Allocation:
    id: int
    ip: str
    ip_alias: str
    port: int
    notes: Optional[str]
    is_default: bool

    @classmethod
    def from_dict(cls, allocation_dict):
        allocation_data = [allocation['attributes'] for allocation in allocation_dict['data']]
        field_names = [field.name for field in fields(cls)]
        kwargs = [{field: allocation.get(field) for field in field_names} for allocation in allocation_data]
        kwargs_dict = {k: v for kwarg in kwargs for k, v in kwarg.items()}
        return cls(**kwargs_dict)

@dataclass
class EggVariable:
    name: str
    description: str
    env_variable: str
    default_value: str
    server_value: str
    is_editable: bool
    rules: str

    @classmethod
    def from_dict(cls, egg_dict):
        variables_data = [egg['attributes'] for egg in egg_dict['data']]
        field_names = [field.name for field in fields(cls)]
        kwargs = [{field: variable.get(field) for field in field_names} for variable in variables_data]
        kwargs_dict = {k: v for kwarg in kwargs for k, v in kwarg.items()}
        return cls(**kwargs_dict)

@dataclass
class Relationships:
    allocations: List[Allocation] = field(default_factory=list)
    variables: List[EggVariable] = field(default_factory=list)

    @classmethod
    def from_dict(cls, relation_dict):
        field_names = [field.name for field in fields(cls)]
        kwargs = {field: relation_dict.get(field) for field in field_names}
        return cls(**kwargs)
    
    def __post_init__(self):
        self.allocations = [Allocation.from_dict(self.allocations)]
        self.variables = [EggVariable.from_dict(self.variables)]

@dataclass
class Server:
    server_owner: bool
    identifier: str
    internal_id: int
    uuid: str
    name: str
    node: str
    is_node_under_maintenance: bool
    sftp_details: SftpDetails
    description: str
    limits: Limits
    invocation: str
    docker_image: str
    egg_features: Optional[str]
    feature_limits: FeatureLimits
    status: Optional[str]
    is_suspended: bool
    is_installing: bool
    is_transferring: bool
    renewable: bool
    renewal: int
    bg: Optional[str]
    relationships: Relationships

    def __post_init__(self):
        self.sftp_details = SftpDetails.from_dict(self.feature_limits)
        self.limits = Limits.from_dict(self.limits)
        self.feature_limits = FeatureLimits.from_dict(self.feature_limits)
        self.relationships = Relationships.from_dict(self.relationships)
