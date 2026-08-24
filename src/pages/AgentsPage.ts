import type { Locator, Page } from '@playwright/test';

/** /lead-management/agents — "Agents". */
export class AgentsPage {
  readonly page: Page;

  readonly showFormerAgentsToggle: Locator;
  readonly teamAverageConversionValue: Locator;
  readonly teamAvgTimeOfConversionValue: Locator;

  static readonly EXPECTED_COLUMN_HEADERS = [
    'Agent Name',
    'Leads',
    'Converted',
    'Conv.Rate',
    'Overdue Leads',
    'Avg Conversion Time',
    'Performance',
  ] as const;

  constructor(page: Page) {
    this.page = page;
    this.showFormerAgentsToggle = page.getByText('Show former agents');
    this.teamAverageConversionValue = page.getByText('Team Average Conversion').locator('..');
    this.teamAvgTimeOfConversionValue = page.getByText('Team Avg Time of Conversion').locator('..');
  }

  async goto(): Promise<void> {
    await this.page.goto('/lead-management/agents', { waitUntil: 'domcontentloaded' });
  }

  async getColumnHeaderTexts(): Promise<string[]> {
    await this.page.getByText(AgentsPage.EXPECTED_COLUMN_HEADERS[0], { exact: true }).first().waitFor({ state: 'visible' });

    const texts: string[] = [];
    for (const header of AgentsPage.EXPECTED_COLUMN_HEADERS) {
      const locator = this.page.getByText(header, { exact: true }).first();
      // eslint-disable-next-line no-await-in-loop
      texts.push((await locator.isVisible()) ? header : '');
    }
    return texts;
  }
}
