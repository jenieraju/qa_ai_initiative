import type { Locator, Page } from '@playwright/test';

/** /lead-management/sources — "Sources". */
export class SourcesPage {
  readonly page: Page;

  readonly topVolumeCard: Locator;
  readonly highestConversionCard: Locator;
  readonly highestRevenueCard: Locator;
  readonly noDataToShowTexts: Locator;

  /** Confirmed live — 9 built-in channels, in this order. */
  static readonly EXPECTED_SOURCE_CHANNELS = [
    'Facebook Ads',
    'Facebook DMs',
    'Website',
    'Instagram DMs',
    'Call',
    'Referral',
    'Others',
    'Newspaper',
    'WhatsApp',
  ] as const;

  constructor(page: Page) {
    this.page = page;
    this.topVolumeCard = page.getByText('Top Volume').locator('..');
    this.highestConversionCard = page.getByText('Highest Conversion').locator('..');
    this.highestRevenueCard = page.getByText('Highest Revenue').locator('..');
    this.noDataToShowTexts = page.getByText('No data to show!');
  }

  async goto(): Promise<void> {
    await this.page.goto('/lead-management/sources', { waitUntil: 'domcontentloaded' });
  }

  sourceRow(channelName: string): Locator {
    // Whichever channel is currently "top" also renders inside the stat
    // cards above the table — .last() reliably targets the table row.
    return this.page.getByText(channelName, { exact: true }).last();
  }
}
