<script>
	import { isAuthenticated } from '$lib/stores.js';
	import Auth from '$lib/components/Auth.svelte';
	import ConfigForm from '$lib/components/ConfigForm.svelte';
</script>

<svelte:head>
	<title>Edit Configuration | Machine Configuration UI</title>
</svelte:head>

{#if $isAuthenticated}
	<ConfigForm />
{:else}
	<Auth />
{/if}
