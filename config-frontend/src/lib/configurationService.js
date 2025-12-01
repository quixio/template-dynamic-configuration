/**
 * Configuration Service - handles all API interactions via server-side proxy
 *
 * All requests go through /api/* routes which proxy to the internal K8s service.
 * This allows the browser to communicate with internal services that aren't
 * directly accessible from outside the cluster.
 */

import { get } from 'svelte/store';
import { quixToken } from './stores.js';

// Use local proxy - the SvelteKit server will forward to the actual API
const getBaseUrl = () => '/api';

const getAuthToken = () => {
	// First, try to get the Quix portal token (when embedded)
	const portalToken = get(quixToken);
	if (portalToken) {
		return portalToken;
	}
	// Fallback to environment SDK token
	if (typeof window !== 'undefined' && window.ENV?.QUIX_SDK_TOKEN) {
		return window.ENV.QUIX_SDK_TOKEN;
	}
	return '';
};

const getHeaders = () => ({
	'Content-Type': 'application/json',
	'authorization': `Bearer ${getAuthToken()}`
});

/**
 * Fetch existing configurations from the API
 * @returns {Promise<Array>} List of configurations
 */
export async function fetchExistingConfigs() {
	const params = new URLSearchParams({
		type: 'printer-config',
		type__operator: '$match',
		sort: 'created_at',
		sort_direction: 'desc',
		limit: '30',
		offset: '0'
	});

	const response = await fetch(`${getBaseUrl()}/configurations?${params}`, {
		headers: getHeaders()
	});

	if (!response.ok) {
		throw new Error(`Failed to fetch configurations: ${response.statusText}`);
	}

	const data = await response.json();
	console.log('API Response:', data);

	// Handle different response formats
	// Could be: array, { items: [] }, { data: [] }, { configurations: [] }
	if (Array.isArray(data)) {
		return data;
	}
	if (data.items && Array.isArray(data.items)) {
		return data.items;
	}
	if (data.data && Array.isArray(data.data)) {
		return data.data;
	}
	if (data.configurations && Array.isArray(data.configurations)) {
		return data.configurations;
	}

	console.warn('Unexpected API response format:', data);
	return [];
}

/**
 * Fetch full configuration by ID
 * @param {string} configId - The configuration ID
 * @returns {Promise<Object>} Full configuration content
 */
export async function fetchFullConfiguration(configId) {
	const response = await fetch(`${getBaseUrl()}/configurations/${configId}/content`, {
		headers: getHeaders()
	});

	if (!response.ok) {
		throw new Error(`Failed to fetch configuration: ${response.statusText}`);
	}

	return response.json();
}

/**
 * Create a new machine configuration
 * @param {string} machineId - Machine identifier
 * @param {string} editorName - Name of the editor
 * @param {number} scalar - Field scalar value
 * @param {Object} mapping - Sensor mapping key-value pairs
 * @returns {Promise<boolean>} Success status
 */
export async function createMachineConfiguration(machineId, editorName, scalar, mapping) {
	const payload = {
		metadata: {
			type: 'printer-config',
			target_key: machineId,
			valid_from: new Date().toISOString(),
			category: 'Printer Settings'
		},
		content: {
			machine_id: machineId,
			editor_name: editorName,
			field_scalar: parseFloat(scalar),
			mapping: mapping
		}
	};

	const response = await fetch(`${getBaseUrl()}/configurations`, {
		method: 'POST',
		headers: getHeaders(),
		body: JSON.stringify(payload)
	});

	return response.ok;
}

/**
 * Update an existing machine configuration
 * @param {string} configId - Configuration ID to update
 * @param {string} machineId - Machine identifier
 * @param {string} editorName - Name of the editor
 * @param {number} scalar - Field scalar value
 * @param {Object} mapping - Sensor mapping key-value pairs
 * @returns {Promise<boolean>} Success status
 */
export async function updateMachineConfiguration(configId, machineId, editorName, scalar, mapping) {
	const payload = {
		content: {
			machine_id: machineId,
			editor_name: editorName,
			field_scalar: parseFloat(scalar),
			mapping: mapping
		}
	};

	const response = await fetch(`${getBaseUrl()}/configurations/${configId}`, {
		method: 'PUT',
		headers: getHeaders(),
		body: JSON.stringify(payload)
	});

	return response.ok;
}

/**
 * Extract unique target keys from configurations
 * @param {Array} configs - List of configurations
 * @returns {Array<string>} Unique target keys
 */
export function getExistingTargetKeys(configs) {
	const keys = new Set();
	for (const config of configs) {
		if (config.metadata?.target_key) {
			keys.add(config.metadata.target_key);
		}
	}
	return Array.from(keys);
}
