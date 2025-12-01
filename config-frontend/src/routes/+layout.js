/** @type {import('./$types').LayoutLoad} */
export async function load({ data }) {
	// Make environment variables available on the client
	if (typeof window !== 'undefined') {
		window.ENV = data.env;
	}
	return data;
}
