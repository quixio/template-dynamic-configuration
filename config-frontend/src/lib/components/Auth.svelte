<script>
	import { onMount, onDestroy } from 'svelte';
	import { page } from '$app/stores';
	import { isAuthenticated, quixToken } from '$lib/stores.js';

	let token = '';
	let error = '';
	let isEmbedded = false;
	let isLoading = true;

	// Get auth token from page data (passed from layout.server.js)
	$: authToken = $page.data?.env?.CONFIG_UI_AUTH_TOKEN || '';

	onMount(() => {
		// Check if running inside Quix portal (iframe)
		isEmbedded = window.self !== window.top;

		if (isEmbedded) {
			// Request token from Quix portal
			window.addEventListener('message', handlePortalMessage);
			window.parent.postMessage({ type: 'REQUEST_AUTH_TOKEN' }, '*');

			// Timeout fallback - show login if no response
			setTimeout(() => {
				if (!$isAuthenticated) {
					isLoading = false;
				}
			}, 2000);
		} else {
			isLoading = false;
		}
	});

	onDestroy(() => {
		if (typeof window !== 'undefined') {
			window.removeEventListener('message', handlePortalMessage);
		}
	});

	function handlePortalMessage(event) {
		if (event.data?.type === 'AUTH_TOKEN' && event.data.token) {
			// Store the Quix token for API calls
			$quixToken = event.data.token;
			$isAuthenticated = true;
			isLoading = false;
		}
	}

	function handleLogin() {
		if (token === authToken) {
			// Store the token for API calls
			$quixToken = token;
			$isAuthenticated = true;
			error = '';
		} else {
			error = 'Invalid auth token; try again.';
		}
	}

	function handleKeyPress(event) {
		if (event.key === 'Enter') {
			handleLogin();
		}
	}
</script>

<div class="auth-container">
	<div class="auth-card">
		<h1>Machine Configuration</h1>

		{#if isLoading}
			<p class="subtitle">Connecting to Quix...</p>
			<div class="loading-spinner"></div>
		{:else}
			<p class="subtitle">Enter your authentication token to continue</p>

			<div class="form-group">
				<label for="token">Token</label>
				<input
					id="token"
					type="password"
					bind:value={token}
					on:keypress={handleKeyPress}
					placeholder="Enter authentication token"
				/>
			</div>

			{#if error}
				<p class="error-text">{error}</p>
			{/if}

			<button class="btn btn-primary full-width" on:click={handleLogin}>
				Login
			</button>
		{/if}
	</div>
</div>

<style>
	.auth-container {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 1rem;
		background-color: #0d1117;
	}

	.auth-card {
		background: #161b22;
		border-radius: 6px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
		padding: 2rem;
		width: 100%;
		max-width: 380px;
		border: 1px solid #30363d;
	}

	h1 {
		text-align: center;
		margin-bottom: 0.5rem;
		color: #e6edf3;
		font-size: 1.5rem;
	}

	.subtitle {
		text-align: center;
		color: #8b949e;
		margin-bottom: 1.5rem;
		font-size: 0.875rem;
	}

	.full-width {
		width: 100%;
	}

	.error-text {
		margin-bottom: 1rem;
	}

	.loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid #30363d;
		border-top-color: #13d194;
		border-radius: 50%;
		margin: 1.5rem auto;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}
</style>
