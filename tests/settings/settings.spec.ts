import { test, expect } from '../fixtures';

// Matrix row: Sl No. 32.

test(
  'settings-defaults-to-calendar-conferencing-tab-with-google-connect',
  { tag: ['@settings', '@smoke', '@sanity', '@regression'] },
  async ({ settingsPage }) => {
    await settingsPage.goto();

    await expect(settingsPage.googleCalendarHeading).toBeVisible();
    await expect(settingsPage.connectButton).toBeVisible();
  },
);
