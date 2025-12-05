import { env } from '$env/dynamic/private';

/** @type {import('./$types').LayoutServerLoad} */
export async function load() {
	const sdkToken = env.Quix__Sdk__Token || '';
	return {
		env: {
			CONFIG_API_BASE_URL: env.CONFIG_API_BASE_URL || 'http://config-api-svc/api/v1',
			// Use SDK token for both UI auth and API calls
			CONFIG_UI_AUTH_TOKEN: sdkToken,
			QUIX_SDK_TOKEN: sdkToken
		}
	};
}
