import { test as base } from '@playwright/test';
import { LoginPage } from '../src/pages/LoginPage';
import { DashboardPage } from '../src/pages/DashboardPage';
import { LeadsListPage } from '../src/pages/LeadsListPage';
import { LeadsAnalyticsPage } from '../src/pages/LeadsAnalyticsPage';
import { AgentsPage } from '../src/pages/AgentsPage';
import { SourcesPage } from '../src/pages/SourcesPage';
import { MyActivitiesPage } from '../src/pages/MyActivitiesPage';
import { ReportsPage } from '../src/pages/ReportsPage';
import { SettingsPage } from '../src/pages/SettingsPage';

type Fixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  leadsListPage: LeadsListPage;
  leadsAnalyticsPage: LeadsAnalyticsPage;
  agentsPage: AgentsPage;
  sourcesPage: SourcesPage;
  myActivitiesPage: MyActivitiesPage;
  reportsPage: ReportsPage;
  settingsPage: SettingsPage;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => use(new LoginPage(page)),
  dashboardPage: async ({ page }, use) => use(new DashboardPage(page)),
  leadsListPage: async ({ page }, use) => use(new LeadsListPage(page)),
  leadsAnalyticsPage: async ({ page }, use) => use(new LeadsAnalyticsPage(page)),
  agentsPage: async ({ page }, use) => use(new AgentsPage(page)),
  sourcesPage: async ({ page }, use) => use(new SourcesPage(page)),
  myActivitiesPage: async ({ page }, use) => use(new MyActivitiesPage(page)),
  reportsPage: async ({ page }, use) => use(new ReportsPage(page)),
  settingsPage: async ({ page }, use) => use(new SettingsPage(page)),
});

export { expect } from '@playwright/test';
