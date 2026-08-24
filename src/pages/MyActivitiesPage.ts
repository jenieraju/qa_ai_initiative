import type { Locator, Page } from '@playwright/test';

/** /lead-management/my-activities — "My Activities". */
export class MyActivitiesPage {
  readonly page: Page;

  readonly tasksTab: Locator;
  readonly meetingsTab: Locator;
  readonly noMatchingActivitiesMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.tasksTab = page.getByRole('tab', { name: 'Tasks' });
    this.meetingsTab = page.getByRole('tab', { name: 'Meetings' });
    this.noMatchingActivitiesMessage = page.getByText('No matching activities found');
  }

  async goto(): Promise<void> {
    await this.page.goto('/lead-management/my-activities', { waitUntil: 'domcontentloaded' });
  }
}
