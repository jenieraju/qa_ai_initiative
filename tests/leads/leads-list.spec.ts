import { test, expect } from '../fixtures';
import { LeadsListPage } from '../../src/pages/LeadsListPage';
import { DashboardPage } from '../../src/pages/DashboardPage';

// Matrix rows: Sl No. 15-18.

test(
  'leads-list-status-column-uses-unified-taxonomy',
  { tag: ['@leads', '@revamp', '@smoke', '@sanity', '@regression'] },
  async ({ leadsListPage }) => {
    await leadsListPage.goto();

    await expect(leadsListPage.statusCells.first()).toBeVisible();
    const statusText = await leadsListPage.statusCells.first().textContent();
    expect(DashboardPage.UNIFIED_STATUS_TAXONOMY).toContain(statusText?.trim());
  },
);

test(
  'leads-list-renders-table-with-confirmed-columns',
  { tag: ['@leads', '@sanity', '@regression'] },
  async ({ leadsListPage }) => {
    await leadsListPage.goto();

    const headerTexts = await leadsListPage.getColumnHeaderTexts();

    expect(headerTexts).toEqual([...LeadsListPage.EXPECTED_COLUMN_HEADERS]);
  },
);

test(
  'leads-list-add-lead-button-visible',
  { tag: ['@leads', '@regression'] },
  async ({ leadsListPage }) => {
    await leadsListPage.goto();

    await expect(leadsListPage.addLeadButton).toBeVisible();
    await expect(leadsListPage.addLeadButton).toBeEnabled();
  },
);

test(
  'leads-list-analytics-tab-shares-same-route-as-list-tab',
  { tag: ['@leads', '@regression'] },
  async ({ page, leadsListPage }) => {
    await leadsListPage.goto();

    await leadsListPage.analyticsTab.click();

    await expect(page).toHaveURL(/\/lead-management\/list$/);
  },
);
