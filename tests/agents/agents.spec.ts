import { test, expect } from '../fixtures';
import { AgentsPage } from '../../src/pages/AgentsPage';

// Matrix rows: Sl No. 23-24.

test(
  'agents-table-columns-match-confirmed-headers',
  { tag: ['@agents', '@smoke', '@sanity', '@regression'] },
  async ({ agentsPage }) => {
    await agentsPage.goto();

    const headerTexts = await agentsPage.getColumnHeaderTexts();

    expect(headerTexts).toEqual([...AgentsPage.EXPECTED_COLUMN_HEADERS]);
  },
);

test(
  'agents-show-former-agents-toggle-visible',
  { tag: ['@agents', '@regression'] },
  async ({ agentsPage }) => {
    await agentsPage.goto();

    await expect(agentsPage.showFormerAgentsToggle).toBeVisible();
  },
);
