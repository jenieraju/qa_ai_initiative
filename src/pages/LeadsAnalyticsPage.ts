import type { Locator, Page } from '@playwright/test';
import { DashboardPage } from './DashboardPage';

/**
 * /lead-management/list, Analytics tab — same route as LeadsListPage, a
 * distinct view reached by clicking the "Analytics" tab (confirmed live
 * 2026-08-24: URL does not change).
 */
export class LeadsAnalyticsPage {
  readonly page: Page;

  readonly locationsChartEmptyMessage: Locator;
  readonly sourceChartHeading: Locator;
  readonly statusChartHeading: Locator;
  readonly statusChartLegendItems: Locator;
  readonly agentsDistributionTable: Locator;

  constructor(page: Page) {
    this.page = page;
    // Confirmed live 2026-08-24: the empty-state message sits 2 parent
    // levels up from its section heading, not 1.
    this.locationsChartEmptyMessage = page.getByText('Leads By Top Locations').locator('../..').getByText('No Lead Data Available');
    this.sourceChartHeading = page.getByText('Leads By Source', { exact: true });
    this.statusChartHeading = page.getByText('Lead Count & Revenue By Status');
    this.statusChartLegendItems = page.getByText(
      new RegExp(`^(${DashboardPage.UNIFIED_STATUS_TAXONOMY.join('|')})$`),
    );
    this.agentsDistributionTable = page.getByText('Leads Distribution By Agents').locator('../..');
  }

  async open(): Promise<void> {
    await this.page.goto('/lead-management/list', { waitUntil: 'domcontentloaded' });
    await this.page.getByRole('tab', { name: 'Analytics' }).click();
  }

  /**
   * Confirmed live 2026-08-24: each status name (e.g. "Prospect") appears
   * exactly twice on this tab — once in the "Lead Count & Revenue By Status"
   * chart legend, once as this table's column header. The chart renders
   * first in DOM order, the table last, so `.last()` per status name
   * reliably targets the table's header rather than the chart's legend.
   */
  agentsDistributionStatusHeader(status: string): Locator {
    return this.page.getByText(status, { exact: true }).last();
  }
}
