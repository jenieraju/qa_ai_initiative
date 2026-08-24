import type { Locator, Page } from '@playwright/test';

/** /lead-management/reports — "Reports & Analytics". */
export class ReportsPage {
  readonly page: Page;

  readonly downloadReportButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.downloadReportButton = page.getByRole('button', { name: 'Download Report' });
  }

  async goto(): Promise<void> {
    await this.page.goto('/lead-management/reports', { waitUntil: 'domcontentloaded' });
  }
}
