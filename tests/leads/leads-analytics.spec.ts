import { test, expect } from '../fixtures';
import { DashboardPage } from '../../src/pages/DashboardPage';

// Matrix rows: Sl No. 19-22.

test(
  'leads-analytics-status-chart-matches-unified-taxonomy',
  { tag: ['@leads-analytics', '@revamp', '@smoke', '@sanity', '@regression'] },
  async ({ leadsAnalyticsPage }) => {
    await leadsAnalyticsPage.open();

    await leadsAnalyticsPage.statusChartHeading.waitFor({ state: 'visible' });
    for (const status of DashboardPage.UNIFIED_STATUS_TAXONOMY) {
      // eslint-disable-next-line no-await-in-loop
      await expect(leadsAnalyticsPage.page.getByText(status, { exact: true }).first()).toBeVisible();
    }
  },
);

test(
  'leads-analytics-agents-distribution-table-matches-unified-taxonomy',
  { tag: ['@leads-analytics', '@revamp', '@sanity', '@regression'] },
  async ({ leadsAnalyticsPage }) => {
    await leadsAnalyticsPage.open();

    await expect(leadsAnalyticsPage.agentsDistributionTable).toBeVisible();
    for (const status of DashboardPage.UNIFIED_STATUS_TAXONOMY) {
      // eslint-disable-next-line no-await-in-loop
      await expect(leadsAnalyticsPage.agentsDistributionStatusHeader(status)).toBeVisible();
    }
  },
);

test(
  'leads-analytics-locations-chart-shows-empty-state',
  { tag: ['@leads-analytics', '@regression'] },
  async ({ leadsAnalyticsPage }) => {
    await leadsAnalyticsPage.open();

    await expect(leadsAnalyticsPage.locationsChartEmptyMessage).toBeVisible();
  },
);

test(
  'leads-analytics-source-chart-label-is-current',
  { tag: ['@leads-analytics', '@revamp', '@regression'] },
  async ({ leadsAnalyticsPage }) => {
    await leadsAnalyticsPage.open();

    await expect(leadsAnalyticsPage.sourceChartHeading).toBeVisible();
    await expect(leadsAnalyticsPage.page.getByText('Leads By Source Distribution')).toHaveCount(0);
  },
);
