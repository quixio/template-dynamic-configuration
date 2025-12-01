import { env } from '$env/dynamic/private';

const getApiUrl = () => env.CONFIG_API_BASE_URL || 'http://config-api-svc/api/v1';

/** @type {import('./$types').RequestHandler} */
export async function GET({ request, url }) {
	const apiUrl = getApiUrl();
	const searchParams = url.searchParams.toString();
	const targetUrl = `${apiUrl}/configurations${searchParams ? `?${searchParams}` : ''}`;

	const authHeader = request.headers.get('authorization') || '';

	console.log('[Proxy] GET configurations');
	console.log('[Proxy] Target URL:', targetUrl);
	console.log('[Proxy] Auth header present:', !!authHeader);

	try {
		const response = await fetch(targetUrl, {
			headers: {
				'Content-Type': 'application/json',
				'authorization': authHeader
			}
		});

		console.log('[Proxy] Response status:', response.status);

		const data = await response.json();
		console.log('[Proxy] Response data:', JSON.stringify(data).substring(0, 200));

		return new Response(JSON.stringify(data), {
			status: response.status,
			headers: { 'Content-Type': 'application/json' }
		});
	} catch (error) {
		console.error('[Proxy] Error:', error);
		return new Response(JSON.stringify({ error: error.message }), {
			status: 500,
			headers: { 'Content-Type': 'application/json' }
		});
	}
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
	const apiUrl = getApiUrl();
	const authHeader = request.headers.get('authorization') || '';
	const body = await request.json();

	const response = await fetch(`${apiUrl}/configurations`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'authorization': authHeader
		},
		body: JSON.stringify(body)
	});

	const data = await response.json().catch(() => ({}));
	return new Response(JSON.stringify(data), {
		status: response.status,
		headers: { 'Content-Type': 'application/json' }
	});
}
