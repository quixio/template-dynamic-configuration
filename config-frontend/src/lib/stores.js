import { writable } from 'svelte/store';

// Authentication state
export const isAuthenticated = writable(false);

// Quix portal token (received via postMessage when embedded)
export const quixToken = writable('');

// Current configuration being edited
export const currentConfig = writable(null);

// List of existing configurations
export const existingConfigs = writable([]);

// Message banner state
export const message = writable({ text: '', type: '', visible: false });

// Global loading state
export const isLoading = writable(false);

let messageTimeout = null;

/**
 * Show a success message (auto-dismisses after 4 seconds)
 * @param {string} text - Message text
 */
export function showSuccess(text) {
	if (messageTimeout) clearTimeout(messageTimeout);
	message.set({ text, type: 'success', visible: true });
	messageTimeout = setTimeout(() => {
		message.set({ text: '', type: '', visible: false });
	}, 4000);
}

/**
 * Show an error message (auto-dismisses after 6 seconds)
 * @param {string} text - Message text
 */
export function showError(text) {
	if (messageTimeout) clearTimeout(messageTimeout);
	message.set({ text, type: 'error', visible: true });
	messageTimeout = setTimeout(() => {
		message.set({ text: '', type: '', visible: false });
	}, 6000);
}

/**
 * Hide the message banner
 */
export function hideMessage() {
	if (messageTimeout) clearTimeout(messageTimeout);
	message.set({ text: '', type: '', visible: false });
}
