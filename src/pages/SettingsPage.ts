import type { Locator, Page } from '@playwright/test';

/** /lead-management/settings — "Settings". */
export class SettingsPage {
  readonly page: Page;

  readonly googleCalendarHeading: Locator;
  readonly connectButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.googleCalendarHeading = page.getByRole('heading', { name: 'Google Calendar Integration' });
    this.connectButton = page.getByRole('button', { name: 'Connect' });
  }

  async goto(): Promise<void> {
    await this.page.goto('/lead-management/settings', { waitUntil: 'domcontentloaded' });
  }
}
