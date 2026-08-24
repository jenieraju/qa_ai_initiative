import { expect, type Locator, type Page } from '@playwright/test';

/**
 * Shared UI assertions and explicit-wait wrappers. Generated tests/page objects
 * should go through these rather than an ad hoc `expect()` call or a fixed
 * `page.waitForTimeout()`, so wait conditions stay consistent project-wide.
 */

export async function waitUntilVisible(locator: Locator, timeoutMs?: number): Promise<void> {
  await expect(locator).toBeVisible({ timeout: timeoutMs });
}

export async function waitUntilClickable(locator: Locator, timeoutMs?: number): Promise<void> {
  await expect(locator).toBeVisible({ timeout: timeoutMs });
  await expect(locator).toBeEnabled({ timeout: timeoutMs });
}

export async function waitForUrl(page: Page, urlOrPattern: string | RegExp, timeoutMs?: number): Promise<void> {
  await page.waitForURL(urlOrPattern, { timeout: timeoutMs });
}

export async function assertText(locator: Locator, expected: string | RegExp): Promise<void> {
  await expect(locator).toHaveText(expected);
}

export async function assertDisabled(locator: Locator): Promise<void> {
  await expect(locator).toBeDisabled();
}

export async function assertEnabled(locator: Locator): Promise<void> {
  await expect(locator).toBeEnabled();
}
