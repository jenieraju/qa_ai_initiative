"""Tracks the active user/context for the current test session."""

from dataclasses import dataclass, field


@dataclass
class SessionState:
    """Holds active profile metadata so steps resolve 'current user' without threading."""

    active_profile: str = "default"
    active_user_email: str = ""
    active_org_id: str = ""
    metadata: dict[str, str] = field(default_factory=dict)

    def set_active_profile(
        self,
        profile_name: str,
        *,
        user_email: str = "",
        org_id: str = "",
    ) -> None:
        self.active_profile = profile_name
        self.active_user_email = user_email
        self.active_org_id = org_id

    def clear(self) -> None:
        self.active_profile = "default"
        self.active_user_email = ""
        self.active_org_id = ""
        self.metadata.clear()


session_state = SessionState()
