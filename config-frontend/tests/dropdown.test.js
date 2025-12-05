import { test, expect } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// Load .env file
const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const AUTH_TOKEN = process.env.Quix__Sdk__Token || 'test-token';
console.log('Using auth token (first 20 chars):', AUTH_TOKEN.substring(0, 20) + '...');

// Mock API response data - matching real API structure { data: [...], links: {}, count: N }
const mockApiResponse = {
	data: [
		{
			id: 'config-1',
			metadata: {
				type: 'printer-config',
				target_key: '3D_PRINTER_1',
				valid_from: '2025-01-01T00:00:00Z',
				category: 'Printer Settings',
				version: 1,
				created_at: '2025-01-01T00:00:00Z'
			}
		},
		{
			id: 'config-2',
			metadata: {
				type: 'printer-config',
				target_key: '3D_PRINTER_2',
				valid_from: '2025-01-02T00:00:00Z',
				category: 'Printer Settings',
				version: 1,
				created_at: '2025-01-02T00:00:00Z'
			}
		}
	],
	links: {},
	count: 2
};

test.describe('Configuration Dropdown', () => {
	test('should display login page initially', async ({ page }) => {
		await page.goto('/');

		// Should see the login form
		await expect(page.locator('h1')).toContainText('Machine Configuration');
		await expect(page.locator('input[type="password"]')).toBeVisible();
		await expect(page.locator('button:has-text("Login")')).toBeVisible();
	});

	test('should login and show config form', async ({ page }) => {
		await page.goto('/');

		// Enter the token and login
		await page.fill('input[type="password"]', AUTH_TOKEN);
		await page.click('button:has-text("Login")');

		// Should see the config form after login
		await expect(page.locator('label:has-text("Select Configuration")')).toBeVisible({ timeout: 5000 });
	});

	test('should populate dropdown with configurations from real API', async ({ page }) => {
		await page.goto('/');

		// Login
		await page.fill('input[type="password"]', AUTH_TOKEN);
		await page.click('button:has-text("Login")');

		// Wait for the dropdown to be visible
		const dropdown = page.locator('#config-select');
		await expect(dropdown).toBeVisible({ timeout: 5000 });

		// Wait for API data to load - should have at least 2 options (Create New + real config)
		await expect(dropdown.locator('option')).toHaveCount(2, { timeout: 10000 });

		// Get all options in the dropdown
		const options = await dropdown.locator('option').allTextContents();
		console.log('Dropdown options:', options);

		// Should have "Create New Configuration" plus configs from real API
		expect(options).toContain('Create New Configuration');
		expect(options).toContain('3D_PRINTER_2'); // Real config from API
		expect(options.length).toBeGreaterThanOrEqual(2);
	});

	test('should show dropdown options count', async ({ page }) => {
		// Capture browser console logs
		page.on('console', msg => console.log('Browser:', msg.text()));

		await page.goto('/');

		// Login
		await page.fill('input[type="password"]', AUTH_TOKEN);
		await page.click('button:has-text("Login")');

		// Wait for the dropdown
		const dropdown = page.locator('#config-select');
		await expect(dropdown).toBeVisible({ timeout: 5000 });

		// Wait for data to load
		await page.waitForTimeout(3000);

		const dropdownHtml = await dropdown.innerHTML();
		console.log('Dropdown HTML:', dropdownHtml);

		const optionCount = await dropdown.locator('option').count();
		console.log('Option count:', optionCount);

		// Should have at least 2 options (Create New + at least one config)
		expect(optionCount).toBeGreaterThanOrEqual(2);
	});
});

test.describe('API Response Debug', () => {
	test('should log actual API response', async ({ page }) => {
		// Don't mock - let it hit the real API
		let apiResponse = null;

		page.on('response', async (response) => {
			if (response.url().includes('/api/configurations')) {
				try {
					apiResponse = await response.json();
					console.log('Actual API Response:', JSON.stringify(apiResponse, null, 2));
				} catch (e) {
					console.log('Response body:', await response.text());
				}
			}
		});

		await page.goto('/');

		// Login
		await page.fill('input[type="password"]', AUTH_TOKEN);
		await page.click('button:has-text("Login")');

		// Wait for API call
		await page.waitForTimeout(3000);

		// Log what we got
		console.log('Final API response:', apiResponse);
	});
});
