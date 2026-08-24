import type { Locator, Page } from '@playwright/test';

/**
 * /login — mobile number + OTP authentication.
 * Selectors sourced from context/ui-auth.md (live DOM inspection, 2026-08-24).
 */
export class LoginPage {
  readonly page: Page;

  readonly mobileNumberInput: Locator;
  readonly termsCheckboxLabel: Locator;
  readonly continueButton: Locator;

  readonly otpInputs: Locator;
  readonly otpContinueButton: Locator;
  readonly resendOtpText: Locator;

  constructor(page: Page) {
    this.page = page;
    this.mobileNumberInput = page.getByRole('textbox', { name: 'Enter your mobile number' });
    this.termsCheckboxLabel = page.locator('label:has(input[data-testid="login_agreeTerms"])');
    this.continueButton = page.getByRole('button', { name: 'Continue' });

    this.otpInputs = page.getByTestId('otpVerify_otpInputs');
    this.otpContinueButton = page.getByRole('button', { name: 'Continue' });
    this.resendOtpText = page.getByText(/Request a new code in|Resend OTP/);
  }

  async goto(): Promise<void> {
    await this.page.goto('/login', { waitUntil: 'domcontentloaded' });
  }

  async enterMobileNumber(mobileNumber: string): Promise<void> {
    await this.mobileNumberInput.fill(mobileNumber);
  }

  async acceptTerms(): Promise<void> {
    await this.termsCheckboxLabel.click();
  }

  async submitMobileNumber(): Promise<void> {
    await this.continueButton.click();
  }

  async enterOtp(otp: string): Promise<void> {
    const digits = otp.split('');
    for (let i = 0; i < digits.length; i += 1) {
      await this.otpInputs.nth(i).fill(digits[i]);
    }
  }

  async submitOtp(): Promise<void> {
    await this.otpContinueButton.click();
  }

  /** Full mobile+OTP login in one call — used by global-setup and the login flow's own test cases. */
  async login(mobileNumber: string, otp: string): Promise<void> {
    await this.goto();
    await this.enterMobileNumber(mobileNumber);
    await this.acceptTerms();
    await this.submitMobileNumber();
    await this.otpInputs.first().waitFor({ state: 'visible' });
    await this.enterOtp(otp);
    await this.submitOtp();
  }
}
