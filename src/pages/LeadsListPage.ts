import type { Locator, Page } from '@playwright/test';

/**
 * /lead-management/list — "Leads" (List tab; Analytics is a tab on the same
 * route, confirmed live 2026-08-24 — not a separate URL).
 */
export class LeadsListPage {
  readonly page: Page;

  readonly listTab: Locator;
  readonly analyticsTab: Locator;
  readonly addLeadButton: Locator;
  readonly statusCells: Locator;

  /** Confirmed live 2026-08-24. */
  static readonly EXPECTED_COLUMN_HEADERS = [
    'Customer Name',
    'Mobile Number',
    'Tags',
    'Source',
    'Assignee',
    'Days Stuck',
    'Status',
    'Actions',
  ] as const;

  constructor(page: Page) {
    this.page = page;
    this.listTab = page.getByRole('tab', { name: 'List' });
    this.analyticsTab = page.getByRole('tab', { name: 'Analytics' });
    this.addLeadButton = page.getByRole('button', { name: 'Add Lead' });
    // Confirmed live 2026-08-24: the leads table is div-based, not a real
    // <table> — no row/table role to scope by. Matches a status *value*
    // exactly, so it can't collide with the "Status" column header text.
    this.statusCells = page.getByText(
      new RegExp(`^(${['Prospect', 'Contacted', 'Market Qualified', 'Parked', 'Sales Qualified', 'Interested', 'In Discussion', 'Onboarded', 'Won', 'Lost'].join('|')})$`),
    );
  }

  async goto(): Promise<void> {
    await this.page.goto('/lead-management/list', { waitUntil: 'domcontentloaded' });
  }

  async getColumnHeaderTexts(): Promise<string[]> {
    await this.page.getByText(LeadsListPage.EXPECTED_COLUMN_HEADERS[0], { exact: true }).first().waitFor({ state: 'visible' });

    const texts: string[] = [];
    for (const header of LeadsListPage.EXPECTED_COLUMN_HEADERS) {
      const locator = this.page.getByText(header, { exact: true }).first();
      // eslint-disable-next-line no-await-in-loop
      texts.push((await locator.isVisible()) ? header : '');
    }
    return texts;
  }
}
