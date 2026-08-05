"""Application-wide constants — no secrets."""

LOGIN_PATH = "/login"
DASHBOARD_PATH = "/dashboard"
GROUPS_PATH = "/groups"
GROUPS_CREATE_PATH = "/groups/create"
HOME_PATH = "/"

# TODO: placeholder — confirm real route with the app team before removing
# @pytest.mark.ignore from tests/test/members/test_member_create.py.
MEMBERS_PATH = "/members"

# Onboarding flow (src/features/authentication/routes.tsx AUTH map in the app repo)
SELECT_ACCOUNT_PATH = "/select-account"
DOCUMENT_UPLOAD_PATH = "/document-upload"
SELECT_PAYMENT_PATH = "/select-payment"
