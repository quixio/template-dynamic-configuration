// Simple script to test the API response
// Run with: node debug-api.js

import 'dotenv/config';

const CONFIG_API_BASE_URL = process.env.CONFIG_API_BASE_URL || 'http://config-api-svc/api/v1';
const TOKEN = process.env.Quix__Sdk__Token || '';

async function testApi() {
	console.log('Testing API at:', CONFIG_API_BASE_URL);
	console.log('Token (first 20 chars):', TOKEN.substring(0, 20) + '...');

	const params = new URLSearchParams({
		type: 'printer-config',
		type__operator: '$match',
		sort: 'created_at',
		sort_direction: 'desc',
		limit: '30',
		offset: '0'
	});

	const url = `${CONFIG_API_BASE_URL}/configurations?${params}`;
	console.log('\nFetching:', url);

	try {
		const response = await fetch(url, {
			headers: {
				'Content-Type': 'application/json',
				'authorization': `Bearer ${TOKEN}`
			}
		});

		console.log('\nResponse status:', response.status);
		console.log('Response headers:', Object.fromEntries(response.headers.entries()));

		const text = await response.text();
		console.log('\nRaw response:', text);

		try {
			const data = JSON.parse(text);
			console.log('\nParsed JSON:', JSON.stringify(data, null, 2));

			// Check structure
			console.log('\n--- Structure Analysis ---');
			console.log('Is array:', Array.isArray(data));
			console.log('Has items:', !!data.items);
			console.log('Has data:', !!data.data);
			console.log('Has configurations:', !!data.configurations);
			console.log('Keys:', Object.keys(data));

			// Try to find configs
			let configs = [];
			if (Array.isArray(data)) configs = data;
			else if (data.items) configs = data.items;
			else if (data.data) configs = data.data;
			else if (data.configurations) configs = data.configurations;

			console.log('\nFound configs count:', configs.length);
			if (configs.length > 0) {
				console.log('First config:', JSON.stringify(configs[0], null, 2));
				console.log('First config keys:', Object.keys(configs[0]));
				if (configs[0].metadata) {
					console.log('First config metadata:', configs[0].metadata);
				}
			}
		} catch (e) {
			console.log('Failed to parse JSON:', e.message);
		}
	} catch (error) {
		console.error('Fetch error:', error);
	}
}

testApi();
