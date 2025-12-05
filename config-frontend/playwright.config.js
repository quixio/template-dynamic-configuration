import { defineConfig } from '@playwright/test';

export default defineConfig({
	webServer: {
		command: 'npm run dev -- --port 5173',
		port: 5173,
		timeout: 120000,
		reuseExistingServer: true
	},
	testDir: 'tests',
	testMatch: /(.+\.)?(test|spec)\.[jt]s/,
	timeout: 30000,
	use: {
		baseURL: 'http://localhost:5173',
		trace: 'on-first-retry'
	}
});
