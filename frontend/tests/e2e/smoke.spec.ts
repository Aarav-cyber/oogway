import { test, expect } from '@playwright/test';

test.describe('Lenny Growth Assistant Smoke Test', () => {
  test('creates session, asks question, views answer and sources', async ({ page }) => {
    // Navigate to frontend
    await page.goto('http://localhost:3000');

    // Expect empty state or header
    await expect(page.locator('header')).toContainText('Lenny Growth Assistant');

    // Type query in chat input
    const input = page.locator('textarea');
    await input.fill("What can Lenny's guests teach us about retention?");
    await input.press('Enter');

    // Wait for response bubble
    await page.waitForSelector('text=Based on');
    await expect(page.locator('body')).toContainText('TRANSCRIPT SOURCES');
  });
});
