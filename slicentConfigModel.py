from typing import List, Literal
from pydantic import BaseModel, Field

class Cloud(BaseModel):
    ram: int
    cpu: int
    hdd: int
    name: str

class NF(BaseModel):
    name: str
    ram: int
    cpu: int
    hdd: int

class Policy(BaseModel):
    type: str
    policy: str

class SliceComposition(BaseModel):
    nf: str
    weight: int

class Slice(BaseModel):
    name: str
    composition: List[SliceComposition]

class ServiceComposition(BaseModel):
    slice: str
    weight: int

class Service(BaseModel):
    name: str
    composition: List[ServiceComposition]

class Slicelet(BaseModel):
    name: str
    service: str
    duration: int

class Config(BaseModel):
    name: str
    description: str
    delay_pattern: Literal["default", "exponential", "normal"] = "default"
    epoch: int = Field(..., description="This applies to slicelets only. TBD to also include slice infra")
    clouds: List[Cloud]
    nfs: List[NF]
    policies: List[Policy]
    slices: List[Slice]
    services: List[Service]
    slicelets: List[Slicelet]