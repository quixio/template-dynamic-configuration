<script>
	import { isAuthenticated, message, hideMessage } from '$lib/stores.js';
	import '../app.css';
</script>

<main>
	{#if $message.visible}
		<div class="message-banner {$message.type}">
			<span>{$message.text}</span>
			<button class="close-btn" on:click={hideMessage}>&times;</button>
		</div>
	{/if}

	<slot />
</main>

<style>
	main {
		min-height: 100vh;
		background-color: #0d1117;
	}

	.message-banner {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		padding: 0.75rem 1rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
		z-index: 1000;
		font-weight: 500;
		font-size: 0.875rem;
	}

	.message-banner.success {
		background-color: #13d194;
		color: #0d1117;
	}

	.message-banner.error {
		background-color: #da3633;
		color: white;
	}

	.close-btn {
		background: none;
		border: none;
		color: inherit;
		font-size: 1.25rem;
		cursor: pointer;
		padding: 0 0.5rem;
		opacity: 0.8;
	}

	.close-btn:hover {
		opacity: 1;
	}
</style>
