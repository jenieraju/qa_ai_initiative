"""Static UI string constants."""

# Login (src/features/authentication/pages/login/Login.tsx in the app repo)
MSG_INVALID_MOBILE_NUMBER = "Invalid mobile number"
MSG_INVALID_OTP = "Oops! please enter a valid code"
TITLE_LOGIN = "Login"
TITLE_OTP_VERIFICATION = "Enter OTP"
SECTION_TITLE_LOGIN = "Login"
SECTION_TITLE_OTP_VERIFICATION = "Verification Code"

# Onboarding — account selection (src/features/authentication/pages/account-selection)
TITLE_REFERRAL_CODE = "Enter referral code"
SECTION_TITLE_REFERRAL_CODE = "Enter your referral code below to redeem your rewards!"
TITLE_SELECT_ACCOUNT = "Select Account"
SECTION_TITLE_SELECT_ACCOUNT = "Help us get to know you"
ACCOUNT_TYPE_INDIVIDUAL = "Individual"
ACCOUNT_TYPE_ORGANIZATION = "Organization"

# Onboarding — document upload / payment selection (organization path)
TITLE_DOCUMENT_UPLOAD = "Document Upload"
SECTION_TITLE_DOCUMENT_UPLOAD = "Upload Your Business Documents"
TITLE_SELECT_PAYMENT = "Select Payment"
SECTION_TITLE_SELECT_PAYMENT = "Let's add your bank account"

# Shared button labels
BTN_CONTINUE = "Continue"
BTN_PROCEED = "Proceed"
BTN_SKIP_REFERRAL = "Skip Referral"
BTN_VERIFY_ACCOUNT = "Verify Account"

# Groups (src/features/groups — web.dev.cofee.life/groups)
TITLE_GROUPS = "Groups"
HEADING_NEW_GROUP = "New group"
PLACEHOLDER_GROUP_NAME = "Eg: Dance Class"
PLACEHOLDER_PAYMENT_COLLECTION_DAY = "Select payment collection day"
PLACEHOLDER_AMOUNT = "0"
PAYMENT_COLLECTION_MONTHLY = "Monthly"
BTN_SAVE_AND_NEXT = "Save and next"
BTN_NEW_GROUP = "New Group"
MSG_GROUP_CREATED = "Group created successfully"

# Members — TODO: all values below are placeholders, not confirmed against
# the live app or its source. Confirm with the app team / discover-locators-
# from-ui before removing @pytest.mark.ignore from test_member_create.py.
TITLE_MEMBERS = "Members"
BTN_ADD_MEMBER = "Add Member"
HEADING_ADD_MEMBER = "Add member"
PLACEHOLDER_MEMBER_NAME = "Eg: Jane Doe"
PLACEHOLDER_MEMBER_MOBILE_NUMBER = "Enter mobile number"
BTN_SAVE_MEMBER = "Save"
MSG_MEMBER_CREATED = "Member added successfully"

# Quick Collect (/quick-collect/create-link, /quick-collect/success)
# All strings confirmed against the live dev app — see context_docs/quick-collect.md.
TITLE_QUICK_COLLECT = "Quick Collect"
HEADING_QUICK_COLLECT = "Quick Collect"
HEADING_QUICK_COLLECT_AMOUNT = "Enter amount"
HEADING_QUICK_COLLECT_PAYERS = "Add Payers"
PLACEHOLDER_QUICK_COLLECT_AMOUNT = "Enter Amount"
PLACEHOLDER_QUICK_COLLECT_NOTE = "Eg: Admission fee for Batch 7"
PLACEHOLDER_QUICK_COLLECT_SEARCH_PAYER = "Search by name"
CHK_QUICK_COLLECT_SUPPRESS_NOTIFICATIONS = "Do not send payment link to payers"
# The CTA is "Send" normally and "Create" once notifications are suppressed.
BTN_QUICK_COLLECT_SEND = "Send"
BTN_QUICK_COLLECT_CREATE = "Create"
BTN_QUICK_COLLECT_CLEAR = "Clear"
BTN_CONFIRM = "Confirm"
BTN_CANCEL = "Cancel"
BTN_QUICK_COLLECT_CREATE_NEW_LINK = "Create New Link"
BTN_QUICK_COLLECT_GO_TO_HOME = "Go To Home"
MSG_QUICK_COLLECT_CONFIRM_DIALOG = "Are you sure you want to create the payment link?"
MSG_QUICK_COLLECT_LINK_CREATED = "Payment link created successfully!"
# Static helper text under Fee Amount — always visible, never turns red.
# An out-of-range amount is signalled by disabling the CTA, not by an error.
HINT_QUICK_COLLECT_AMOUNT_RANGE = "Allowed amount is between 2 and 200000"
MSG_QUICK_COLLECT_SUCCESS_PREFIX = "Your payment link successfully created for"
TESTID_QUICK_COLLECT_SUCCESS_TEXT = "quick_collect_success_text"

# Quick Collect amount bounds, from the on-screen validation copy.
QUICK_COLLECT_AMOUNT_MIN = 2
QUICK_COLLECT_AMOUNT_MAX = 200000
