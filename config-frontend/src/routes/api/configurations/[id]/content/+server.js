import { env } from '$env/dynamic/private';

const getApiUrl = () => env.CONFIG_API_BASE_URL || 'http://config-api-svc/api/v1';

/** @type {import('./$types').RequestHandler} */
export async function GET({ request, params }) {
	const apiUrl = getApiUrl();
	const authHeader = request.headers.get('authorization') || '';

	const response = await fetch(`${apiUrl}/configurations/${params.id}/content`, {
		headers: {
			'Content-Type': 'application/json',
			'authorization': authHeader
		}
	});

	const data = await response.json();
	return new Response(JSON.stringify(data), {
		status: response.status,
		headers: { 'Content-Type': 'application/json' }
	});
}
