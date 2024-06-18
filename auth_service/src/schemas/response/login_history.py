from pydantic import BaseModel

from auth_service.src.schemas.mixins import IdMixin, ORMMixin, UserAgentMixin, UserIdMixin
from auth_service.src.utils.date_format import utc_plus3


class LoginHistoryResponse(IdMixin, UserIdMixin, UserAgentMixin, ORMMixin):
    login_at: utc_plus3
    logout_at: utc_plus3 | None


class LoginHistoryResponseList(BaseModel):
    records: list[LoginHistoryResponse]
