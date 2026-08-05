"""Static UI string constants."""

MSG_SESSION_EXPIRED = "Session expired"
MSG_LOGOUT_SUCCESS = "You have been logged out"
MSG_LOGIN_SUCCESS = "Welcome"

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
