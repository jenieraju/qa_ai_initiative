import { defineConfig, devices } from '@playwright/test';
import { config } from './config/config';

export default defineConfig({
  testDir: './tests',
  timeout: config.timeouts.actionMs * 3,
  expect: {
    timeout: config.timeouts.expectMs,
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  // Capped locally — uncapped local parallelism caused real navigation
  // timeouts under resource contention in an earlier dogfood run.
  workers: process.env.CI ? undefined : 4,
  reporter: [
    ['list'],
    ['allure-playwright', { resultsDir: 'allure-results' }],
  ],
  globalSetup: './global-setup.ts',
  use: {
    baseURL: config.baseUrl,
    navigationTimeout: config.timeouts.navigationMs,
    actionTimeout: config.timeouts.actionMs,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: 'auth/storageState.json' },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'], storageState: 'auth/storageState.json' },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'], storageState: 'auth/storageState.json' },
    },
  ],
});
