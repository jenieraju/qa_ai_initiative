import { test, expect } from '../fixtures';
import { SourcesPage } from '../../src/pages/SourcesPage';

// Matrix rows: Sl No. 25-26, 33.

test(
  'sources-built-in-channel-list-matches-confirmed-set',
  { tag: ['@sources', '@smoke', '@sanity', '@regression'] },
  async ({ sourcesPage }) => {
    await sourcesPage.goto();

    for (const channel of SourcesPage.EXPECTED_SOURCE_CHANNELS) {
      // eslint-disable-next-line no-await-in-loop
      await expect(sourcesPage.sourceRow(channel)).toBeVisible();
    }
  },
);

test(
  'sources-top-cards-show-live-data-not-empty-state',
  { tag: ['@sources', '@sanity', '@regression'] },
  async ({ sourcesPage }) => {
    await sourcesPage.goto();

    await expect(sourcesPage.topVolumeCard).toContainText('Website');
    await expect(sourcesPage.noDataToShowTexts).toHaveCount(0);
  },
);

test(
  'sources-custom-source-gets-initials-or-fixed-icon',
  { tag: ['@sources', '@regression'] },
  async ({ sourcesPage }) => {
    test.skip(
      true,
      'The "add a new source" UI flow has not been discovered. Row 33 in context/ui-test-case-matrix.md.',
    );
    await sourcesPage.goto();
  },
);
