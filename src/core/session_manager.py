"""Singleton browser session management."""

from playwright.sync_api import Browser, BrowserContext, Page, Playwright


class SessionManager:
    """Reuses browser contexts across tests per user/credential profile."""

    _instance: "SessionManager | None" = None

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._contexts: dict[str, BrowserContext] = {}
        self._pages: dict[str, Page] = {}

    @classmethod
    def instance(cls) -> "SessionManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset singleton — primarily for test isolation between sessions."""
        if cls._instance is not None:
            cls._instance.close_all()
            cls._instance = None

    def bind_playwright(self, playwright: Playwright, browser: Browser) -> None:
        self._playwright = playwright
        self._browser = browser

    def get_or_create_context(
        self,
        profile_name: str,
        *,
        storage_state: str | None = None,
        **context_kwargs,
    ) -> BrowserContext:
        if profile_name in self._contexts:
            return self._contexts[profile_name]
        if self._browser is None:
            raise RuntimeError("SessionManager browser is not initialized.")
        kwargs = dict(context_kwargs)
        if storage_state:
            kwargs["storage_state"] = storage_state
        context = self._browser.new_context(**kwargs)
        self._contexts[profile_name] = context
        return context

    def get_or_create_page(self, profile_name: str) -> Page:
        if profile_name in self._pages and not self._pages[profile_name].is_closed():
            return self._pages[profile_name]
        context = self._contexts.get(profile_name)
        if context is None:
            raise RuntimeError(f"No context registered for profile '{profile_name}'.")
        page = context.new_page()
        self._pages[profile_name] = page
        return page

    def get_active_page(self, profile_name: str) -> Page | None:
        page = self._pages.get(profile_name)
        if page is not None and not page.is_closed():
            return page
        return None

    def close_all(self) -> None:
        for page in self._pages.values():
            if not page.is_closed():
                page.close()
        for context in self._contexts.values():
            context.close()
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.stop()
        self._pages.clear()
        self._contexts.clear()
        self._browser = None
        self._playwright = None
