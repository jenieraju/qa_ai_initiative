import { chromium } from '@playwright/test';
import { LoginPage } from './src/pages/LoginPage';
import { config } from './config/config';

/**
 * One-time authenticated-session setup, run once before the whole suite.
 * Every test's browser context loads the resulting auth/storageState.json
 * instead of repeating the mobile+OTP login flow per test.
 *
 * Exception: the login flow's own test cases (tests/login/login.spec.ts)
 * exercise the real UI flow directly and do NOT use this cached shortcut.
 *
 * Auth is token-based (localStorage `token`/`refresh_token`, sessionStorage
 * `branch_session` — see context/ui-auth.md), not a cookie, so the storage
 * state captured here grants access to /lead-management/* regardless of
 * which page the login flow lands on by default.
 */
export default async function globalSetup(): Promise<void> {
  const mobileNumber = process.env.TEST_MOBILE_NUMBER;
  const otp = process.env.TEST_OTP;

  if (!mobileNumber || !otp) {
    throw new Error(
      'TEST_MOBILE_NUMBER and TEST_OTP must be set (see .env.example) — global-setup cannot ' +
        'establish an authenticated session without them.',
    );
  }

  const browser = await chromium.launch();
  const context = await browser.newContext({ baseURL: config.baseUrl });
  const page = await context.newPage();

  const loginPage = new LoginPage(page);
  await loginPage.login(mobileNumber, otp);
  await page.waitForURL(/\/dashboard/, { timeout: config.timeouts.navigationMs });

  await context.storageState({ path: 'auth/storageState.json' });
  await browser.close();
}
