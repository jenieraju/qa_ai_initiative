import { test, expect } from '../fixtures';

// Matrix rows: Sl No. 29-31.

test(
  'reports-download-disabled-until-required-date-range-set',
  { tag: ['@reports', '@smoke', '@sanity', '@regression'] },
  async ({ reportsPage }) => {
    await reportsPage.goto();

    await expect(reportsPage.downloadReportButton).toBeDisabled();
  },
);

test(
  'reports-lead-status-filter-reflects-unified-taxonomy',
  { tag: ['@reports', '@revamp', '@regression'] },
  async ({ reportsPage }) => {
    await reportsPage.goto();

    await expect(reportsPage.page.getByText('Prospect', { exact: true })).toBeVisible();
    await expect(reportsPage.page.getByText('Contacted', { exact: true })).toBeVisible();
    await expect(reportsPage.page.getByText('+8')).toBeVisible();
  },
);

test(
  'reports-source-filter-matches-sources-page-channel-list',
  { tag: ['@reports', '@sanity', '@regression'] },
  async ({ reportsPage }) => {
    await reportsPage.goto();

    await expect(reportsPage.page.getByText('Facebook Ads', { exact: true })).toBeVisible();
    await expect(reportsPage.page.getByText('Facebook DMs', { exact: true })).toBeVisible();
    await expect(reportsPage.page.getByText('+7')).toBeVisible();
  },
);
