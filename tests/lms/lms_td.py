"""Test data for LMS matrix rows (context/ui-test-case-matrix.md)."""

import pytest


class LeadsListTestData:
    ZERO_MATCH_SEARCH_TERMS = [
        pytest.param("zzz-no-match-9812", id="leads_list_zero_match_search"),
    ]


class AdSourcesTestData:
    ZERO_MATCH_SEARCH_TERMS = [
        # Figma-documented empty-state example (LMS.pdf) - not agent-invented.
        pytest.param("FB Campaign", id="ad_sources_zero_match_search"),
    ]


class AuthSessionRedirectTestData:
    """Rows 4, 9, 15, 19, 26 - identical shape, only the target path differs."""

    UNAUTHENTICATED_REDIRECT_PATHS = [
        pytest.param("lead-management/dashboard", id="sl04_dashboard"),
        pytest.param("lead-management/list", id="sl09_leads_list"),
        pytest.param("lead-management/list", id="sl15_leads_analytics"),
        pytest.param("lead-management/agents", id="sl19_agents"),
        pytest.param("lead-management/sources", id="sl26_sources"),
    ]
