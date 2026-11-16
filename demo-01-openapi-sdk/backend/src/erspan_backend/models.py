from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress


class APIModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErspanSource(APIModel):
    interfaces: list[str] = Field(min_length=1)
    direction: Literal["rx", "tx", "both"] = "both"


class ErspanDestination(APIModel):
    ip_address: IPvAnyAddress
    origin_ip_address: IPvAnyAddress
    erspan_id: int = Field(ge=1, le=1023)
    vrf: str = "default"
    ttl: int = Field(default=64, ge=1, le=255)
    dscp: int = Field(default=0, ge=0, le=63)


class ErspanSession(APIModel):
    name: str = Field(min_length=1)
    description: str = Field(default="", max_length=32)
    enabled: bool = True

    source: ErspanSource
    destination: ErspanDestination


class ErrorModel(APIModel):
    title: str
    status: int
    detail: str = Field(default="")
