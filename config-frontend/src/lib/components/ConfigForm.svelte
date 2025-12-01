<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import SensorMapping from './SensorMapping.svelte';
	import {
		existingConfigs,
		currentConfig,
		showSuccess,
		showError
	} from '$lib/stores.js';
	import {
		fetchExistingConfigs,
		fetchFullConfiguration,
		createMachineConfiguration,
		updateMachineConfiguration,
		getExistingTargetKeys
	} from '$lib/configurationService.js';

	let machineId = '';
	let editorName = '';
	let fieldScalar = '1.0';
	let mappings = [{ key: '', value: '' }];
	let selectedConfig = '';
	let configId = null;
	let isLoading = true;
	let isSaving = false;

	$: configMachineId = $page.params.machineId;

	onMount(async () => {
		await loadConfigs();
	});

	$: if (configMachineId && $existingConfigs.length > 0) {
		loadConfigByMachineId(configMachineId);
	}

	async function loadConfigs() {
		try {
			console.log('[ConfigForm] Loading configs...');
			const configs = await fetchExistingConfigs();
			console.log('[ConfigForm] Received configs:', configs);
			console.log('[ConfigForm] Configs length:', configs?.length);
			$existingConfigs = configs;
			console.log('[ConfigForm] Target keys:', getExistingTargetKeys(configs));
			isLoading = false;
		} catch (err) {
			console.error('[ConfigForm] Error loading configs:', err);
			showError('Failed to load configurations');
			isLoading = false;
		}
	}

	async function loadConfigByMachineId(targetMachineId) {
		const config = $existingConfigs.find(
			(c) => c.metadata?.target_key === targetMachineId
		);

		if (config) {
			try {
				const fullConfig = await fetchFullConfiguration(config.id);
				configId = config.id;
				machineId = fullConfig.machine_id || '';
				editorName = fullConfig.editor_name || '';
				fieldScalar = String(fullConfig.field_scalar || 1.0);

				if (fullConfig.mapping && Object.keys(fullConfig.mapping).length > 0) {
					mappings = Object.entries(fullConfig.mapping).map(([key, value]) => ({
						key,
						value
					}));
				}

				selectedConfig = targetMachineId;
			} catch (err) {
				showError('Failed to load configuration details');
			}
		}
	}

	function handleConfigSelect(event) {
		const value = event.target.value;

		if (value === 'new') {
			resetForm();
			goto('/');
		} else if (value) {
			goto(`/config/${value}`);
		}
	}

	function resetForm() {
		machineId = '';
		editorName = '';
		fieldScalar = '1.0';
		mappings = [{ key: '', value: '' }];
		configId = null;
		selectedConfig = '';
	}

	async function handleSubmit() {
		// Validation
		if (!machineId.trim()) {
			showError('Machine ID is required');
			return;
		}

		if (!editorName.trim()) {
			showError('Editor Name is required');
			return;
		}

		// Build mapping object
		const mappingObj = {};
		for (const m of mappings) {
			if (m.key.trim() && m.value.trim()) {
				mappingObj[m.key.trim()] = m.value.trim();
			}
		}

		const existingKeys = getExistingTargetKeys($existingConfigs);
		const isUpdate = configId !== null;

		// Check for duplicate machine ID before saving
		if (!isUpdate && existingKeys.includes(machineId)) {
			showError(`Machine ID "${machineId}" already exists. Select it from the dropdown to edit.`);
			return;
		}

		isSaving = true;

		try {
			if (isUpdate) {
				// Update existing configuration
				const success = await updateMachineConfiguration(
					configId,
					machineId,
					editorName,
					fieldScalar,
					mappingObj
				);

				if (success) {
					showSuccess('Configuration updated successfully!');
					await loadConfigs();
				} else {
					showError('Failed to update configuration');
				}
			} else {
				// Create new configuration
				const success = await createMachineConfiguration(
					machineId,
					editorName,
					fieldScalar,
					mappingObj
				);

				if (success) {
					showSuccess('Configuration created successfully!');
					await loadConfigs();
					goto(`/config/${machineId}`);
				} else {
					showError('Failed to create configuration');
				}
			}
		} catch (err) {
			showError(`Error: ${err.message}`);
		} finally {
			isSaving = false;
		}
	}

	// Reactive declaration - updates when $existingConfigs changes
	$: configOptions = getExistingTargetKeys($existingConfigs);
</script>

<div class="container">
	{#if isLoading}
		<div class="loading-overlay">
			<div class="loading-content">
				<div class="loading-spinner"></div>
				<p>Loading configurations...</p>
			</div>
		</div>
	{/if}

	<div class="card">
		<h1>Machine Configuration</h1>

		<div class="form-group">
			<label for="config-select">Select Configuration</label>
			<select
				id="config-select"
				value={selectedConfig || 'new'}
				on:change={handleConfigSelect}
			>
				<option value="new">Create New Configuration</option>
				{#each configOptions as key}
					<option value={key}>{key}</option>
				{/each}
			</select>
		</div>

		<hr />

		<div class="form-group">
			<label for="machine-id">Machine ID *</label>
			<input
				id="machine-id"
				type="text"
				bind:value={machineId}
				placeholder="e.g., 3D_PRINTER_2"
				disabled={configId !== null}
			/>
			{#if configId !== null}
				<p class="hint">Machine ID cannot be changed after creation</p>
			{/if}
		</div>

		<div class="form-group">
			<label for="editor-name">Editor Name *</label>
			<input
				id="editor-name"
				type="text"
				bind:value={editorName}
				placeholder="Your name"
			/>
		</div>

		<div class="form-group">
			<label for="field-scalar">Field Scalar</label>
			<input
				id="field-scalar"
				type="text"
				bind:value={fieldScalar}
				placeholder="1.0"
			/>
		</div>

		<SensorMapping bind:mappings />

		<button class="btn btn-primary" on:click={handleSubmit} disabled={isSaving}>
			{#if isSaving}
				<span class="spinner"></span>
				{configId !== null ? 'Updating...' : 'Creating...'}
			{:else}
				{configId !== null ? 'Update Configuration' : 'Create Configuration'}
			{/if}
		</button>
	</div>
</div>

<style>
	.loading-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(13, 17, 23, 0.9);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 100;
	}

	.loading-content {
		text-align: center;
		color: #8b949e;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 3px solid #30363d;
		border-top-color: #13d194;
		border-radius: 50%;
		margin: 0 auto 1rem;
		animation: spin 0.8s linear infinite;
	}

	hr {
		border: none;
		border-top: 1px solid #30363d;
		margin: 1.25rem 0;
	}

	.hint {
		color: #8b949e;
		font-size: 0.75rem;
		margin-top: 0.25rem;
	}

	#machine-id:disabled {
		background-color: #21262d;
		color: #8b949e;
		cursor: not-allowed;
	}

	.spinner {
		display: inline-block;
		width: 14px;
		height: 14px;
		border: 2px solid #0d1117;
		border-top-color: transparent;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
		margin-right: 0.5rem;
		vertical-align: middle;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	button:disabled {
		opacity: 0.7;
		cursor: not-allowed;
	}
</style>
