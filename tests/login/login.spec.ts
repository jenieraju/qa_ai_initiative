import { test, expect } from '../fixtures';

// Login flow's own test cases exercise the real UI directly — never the
// cached storageState shortcut. Matrix rows: Sl No. 1-7.

test.describe('Login — unauthenticated flow', () => {
  test.use({ storageState: { cookies: [], origins: [] } });

  test(
    'login-valid-mobile-and-otp-success',
    { tag: ['@login', '@smoke', '@sanity', '@regression'] },
    async ({ page, loginPage }) => {
      const mobileNumber = process.env.TEST_MOBILE_NUMBER;
      const otp = process.env.TEST_OTP;
      test.skip(!mobileNumber || !otp, 'TEST_MOBILE_NUMBER / TEST_OTP not set — see .env.example');

      await loginPage.login(mobileNumber!, otp!);

      await expect(page).toHaveURL(/\/dashboard/);
    },
  );

  test(
    'login-mobile-number-below-10-digits-blocks-continue',
    { tag: ['@login', '@regression'] },
    async ({ loginPage }) => {
      await loginPage.goto();
      await loginPage.enterMobileNumber('98765');
      await loginPage.acceptTerms();

      await expect(loginPage.continueButton).toBeDisabled();
    },
  );

  test(
    'login-terms-checkbox-unchecked-blocks-continue',
    { tag: ['@login', '@regression'] },
    async ({ loginPage }) => {
      await loginPage.goto();
      await loginPage.enterMobileNumber('9847123456');

      await expect(loginPage.continueButton).toBeDisabled();
    },
  );

  test(
    'login-mobile-field-enforces-10-digit-maxlength',
    { tag: ['@login', '@regression'] },
    async ({ loginPage }) => {
      await loginPage.goto();
      await loginPage.enterMobileNumber('98471234567');

      await expect(loginPage.mobileNumberInput).toHaveValue(/^\d{10}$/);
    },
  );

  test(
    'otp-all-six-digits-required-to-enable-continue',
    { tag: ['@login', '@regression'] },
    async ({ loginPage }) => {
      const mobileNumber = process.env.TEST_MOBILE_NUMBER;
      const otp = process.env.TEST_OTP;
      test.skip(!mobileNumber || !otp, 'TEST_MOBILE_NUMBER / TEST_OTP not set — see .env.example');

      await loginPage.goto();
      await loginPage.enterMobileNumber(mobileNumber!);
      await loginPage.acceptTerms();
      await loginPage.submitMobileNumber();
      await loginPage.otpInputs.first().waitFor({ state: 'visible' });

      await loginPage.enterOtp(otp!.slice(0, 5));

      await expect(loginPage.otpContinueButton).toBeDisabled();
    },
  );

  test(
    'otp-resend-control-cooldown-then-actionable',
    { tag: ['@login', '@regression'] },
    async ({ loginPage }) => {
      const mobileNumber = process.env.TEST_MOBILE_NUMBER;
      const otp = process.env.TEST_OTP;
      test.skip(!mobileNumber || !otp, 'TEST_MOBILE_NUMBER / TEST_OTP not set — see .env.example');
      test.slow(); // waits out a real ~30-35s cooldown

      await loginPage.goto();
      await loginPage.enterMobileNumber(mobileNumber!);
      await loginPage.acceptTerms();
      await loginPage.submitMobileNumber();
      await loginPage.otpInputs.first().waitFor({ state: 'visible' });

      await expect(loginPage.resendOtpText).toHaveText(/Request a new code in/);
      await expect(loginPage.resendOtpText).toHaveText(/Resend OTP/, { timeout: 40_000 });
    },
  );

  test(
    'unauthenticated-direct-access-redirects-to-login',
    { tag: ['@login', '@sanity', '@regression'] },
    async ({ page }) => {
      await page.goto('/lead-management/dashboard');

      await expect(page).toHaveURL(/\/login/);
    },
  );
});
