"""Application-wide constants — no secrets."""

LOGIN_PATH = "/login"
GROUPS_PATH = "/groups"
GROUPS_CREATE_PATH = "/groups/create"

# Confirmed from the app bundle's route map (web.dev.cofee.life main.887a1bd7.js):
# MEMBERS list, ADD_MEMBER is its own route (not a modal), plus a details route.
MEMBERS_PATH = "/members"
MEMBERS_ADD_PATH = "/members/add"

# Quick Collect — one-off payment links (see context_docs/quick-collect.md)
QUICK_COLLECT_CREATE_LINK_PATH = "/quick-collect/create-link"
QUICK_COLLECT_SUCCESS_PATH = "/quick-collect/success"

# Onboarding flow (src/features/authentication/routes.tsx AUTH map in the app repo)
SELECT_ACCOUNT_PATH = "/select-account"
# Added app-side after this suite was written; the individual onboarding flow now
# routes here instead of straight to /groups. Not yet automated — see
# context_docs/authentication-onboarding.md and README.md -> "Next steps".
SELECT_CATEGORY_PATH = "/select-category"
CREATE_BRANCH_PATH = "/create-branch"
DOCUMENT_UPLOAD_PATH = "/document-upload"
SELECT_PAYMENT_PATH = "/select-payment"
