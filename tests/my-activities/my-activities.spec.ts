import { test, expect } from '../fixtures';

// Matrix rows: Sl No. 27-28.

test(
  'my-activities-empty-state-shows-no-matching-message',
  { tag: ['@my-activities', '@smoke', '@sanity', '@regression'] },
  async ({ myActivitiesPage }) => {
    await myActivitiesPage.goto();

    await expect(myActivitiesPage.noMatchingActivitiesMessage).toBeVisible();
  },
);

test(
  'my-activities-date-range-options-are-page-specific',
  { tag: ['@my-activities', '@regression'] },
  async ({ myActivitiesPage, page }) => {
    await myActivitiesPage.goto();

    await expect(page.getByText('Today', { exact: true })).toBeVisible();
    await expect(page.getByText('This week', { exact: true })).toBeVisible();
    await expect(page.getByText('This Month', { exact: true })).toBeVisible();
    await expect(page.getByText('Custom', { exact: true })).toBeVisible();
    await expect(page.getByText('Last Month', { exact: true })).not.toBeVisible();
  },
);
