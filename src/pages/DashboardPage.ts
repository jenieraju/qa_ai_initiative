import type { Locator, Page } from '@playwright/test';

/**
 * /lead-management/dashboard — "Leads Dashboard".
 * Locators are text/role-based — no data-testid dump was done for this page
 * beyond the org-avatar menu trigger (see context/ui-context.md's Open Questions).
 */
export class DashboardPage {
  readonly page: Page;

  readonly stuckLeadsThresholdButton: Locator;
  readonly mostAffectedStatusText: Locator;
  readonly conversionFunnelEmptyMessage: Locator;
  readonly conversionFunnelList: Locator;
  readonly newLeadsValue: Locator;

  /** The unified 10-status taxonomy — confirmed live 2026-08-24 on the Dashboard's
   * Conversion Funnel, the LMS revamp this project is built to verify. */
  static readonly UNIFIED_STATUS_TAXONOMY = [
    'Prospect',
    'Contacted',
    'Market Qualified',
    'Parked',
    'Sales Qualified',
    'Interested',
    'In Discussion',
    'Onboarded',
    'Won',
    'Lost',
  ] as const;

  constructor(page: Page) {
    this.page = page;
    this.stuckLeadsThresholdButton = page.getByRole('button', { name: /\d\+\s*days?/i });
    this.mostAffectedStatusText = page.getByText(/Most Affected Status:/);
    this.conversionFunnelEmptyMessage = page.getByText('No Lead Data Available');
    // Confirmed live 2026-08-24: each <li> has 3 <span> children — a
    // decorative aria-hidden color dot (empty text), the stage name, then
    // the count. The stage name is always the 2nd child.
    this.conversionFunnelList = page.getByRole('list').locator('> li > span:nth-child(2)');
    this.newLeadsValue = page.getByText('New Leads', { exact: true }).locator('..');
  }

  async goto(): Promise<void> {
    await this.page.goto('/lead-management/dashboard', { waitUntil: 'domcontentloaded' });
  }

  async getConversionFunnelStageNames(): Promise<string[]> {
    await this.conversionFunnelList.first().waitFor({ state: 'visible' });
    return this.conversionFunnelList.allTextContents();
  }
}
