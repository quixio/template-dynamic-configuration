<script>
	export let mappings = [{ key: '', value: '' }];

	function addMapping() {
		mappings = [...mappings, { key: '', value: '' }];
	}

	function removeMapping(index) {
		if (mappings.length > 1) {
			mappings = mappings.filter((_, i) => i !== index);
		}
	}

	function updateMapping(index, field, value) {
		mappings[index][field] = value;
		mappings = mappings; // Trigger reactivity
	}
</script>

<div class="mapping-section">
	<h2>Sensor Mappings</h2>
	<p class="hint">Map sensor keys to their display names</p>

	<div class="mapping-table">
		<div class="mapping-header">
			<span>Sensor Key</span>
			<span>Display Name</span>
			<span></span>
		</div>

		{#each mappings as mapping, index}
			<div class="mapping-row">
				<input
					type="text"
					value={mapping.key}
					on:input={(e) => updateMapping(index, 'key', e.target.value)}
					placeholder="e.g., T001"
				/>
				<input
					type="text"
					value={mapping.value}
					on:input={(e) => updateMapping(index, 'value', e.target.value)}
					placeholder="e.g., sensor_1"
				/>
				<button
					class="btn btn-danger btn-small"
					on:click={() => removeMapping(index)}
					disabled={mappings.length === 1}
					title={mappings.length === 1 ? 'At least one mapping is required' : 'Remove mapping'}
				>
					&times;
				</button>
			</div>
		{/each}
	</div>

	<button class="btn btn-secondary" on:click={addMapping}>
		+ Add Mapping
	</button>
</div>

<style>
	.mapping-section {
		margin-bottom: 1.25rem;
	}

	h2 {
		margin-bottom: 0.25rem;
		color: #e6edf3;
		font-size: 1rem;
		font-weight: 500;
	}

	.hint {
		color: #8b949e;
		font-size: 0.75rem;
		margin-bottom: 0.75rem;
	}

	.mapping-table {
		margin-bottom: 0.75rem;
	}

	.mapping-header {
		display: grid;
		grid-template-columns: 1fr 1fr 44px;
		gap: 0.5rem;
		padding: 0.5rem 0;
		font-weight: 500;
		font-size: 0.75rem;
		color: #8b949e;
		border-bottom: 1px solid #30363d;
		margin-bottom: 0.5rem;
	}

	.mapping-row {
		display: grid;
		grid-template-columns: 1fr 1fr 44px;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.mapping-row input {
		padding: 0.5rem 0.625rem;
		border: 1px solid #30363d;
		border-radius: 6px;
		font-size: 0.875rem;
		background-color: #0d1117;
		color: #e6edf3;
	}

	.mapping-row input::placeholder {
		color: #484f58;
	}

	.mapping-row input:focus {
		outline: none;
		border-color: #13d194;
		background-color: #0d1117;
		box-shadow: 0 0 0 3px rgba(19, 209, 148, 0.15);
	}

	.btn-small {
		padding: 0.5rem;
		font-size: 1rem;
		line-height: 1;
	}

	.btn-small:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}
</style>
