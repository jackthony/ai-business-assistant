import re
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}\Z")
TENANT_PATTERN = re.compile(r"^[a-z0-9_]{1,32}\Z")
CHANNEL_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,19}\Z")
MAX_CONTENT_CHARS = 1000


class InboundEvent(BaseModel):
    model_config = {"frozen": True}

    tenant: str
    user_id: str
    type: Literal["text", "media", "voice"]
    content: str | None = Field(None, max_length=MAX_CONTENT_CHARS)
    channel: str

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        if not ID_PATTERN.match(v):
            raise ValueError(f"Invalid user_id format: {v}")
        return v

    @field_validator("tenant")
    @classmethod
    def validate_tenant(cls, v: str) -> str:
        if not TENANT_PATTERN.match(v):
            raise ValueError(f"Invalid tenant format: {v}")
        return v

    @field_validator("channel")
    @classmethod
    def validate_channel(cls, v: str) -> str:
        if not CHANNEL_PATTERN.match(v):
            raise ValueError(f"Invalid channel format: {v}")
        return v


class OutboundReply(BaseModel):
    model_config = {"frozen": True}

    text: str | None = None
    media: bytes | None = None
    template_id: str | None = None
    channel_metadata: dict[str, Any] = Field(default_factory=dict)
