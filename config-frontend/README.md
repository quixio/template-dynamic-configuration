# Machine Configuration UI

A Svelte-based frontend application for managing machine/printer configurations through the Quix Configuration API.

## Features

- Token-based authentication
- Create and edit machine configurations
- Dynamic sensor mapping interface
- Real-time form validation
- Deep linking to specific configurations
- URL-based routing with browser navigation support

## Tech Stack

- **Framework:** SvelteKit
- **Runtime:** Node.js 20
- **Styling:** CSS (no external dependencies)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CONFIG_API_BASE_URL` | Yes | Base URL of the Configuration API |
| `CONFIG_UI_AUTH_TOKEN` | Yes | Token for UI authentication |
| `Quix__Sdk__Token` | Auto | SDK token for API authentication (provided by Quix) |

## Development

### Prerequisites

- Node.js 20 or later
- npm

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The development server will start at `http://localhost:3000`.

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
config-frontend/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── Auth.svelte           # Authentication form
│   │   │   ├── ConfigForm.svelte     # Main configuration form
│   │   │   └── SensorMapping.svelte  # Dynamic sensor mapping table
│   │   ├── configurationService.js   # API integration layer
│   │   └── stores.js                 # Svelte stores for state
│   ├── routes/
│   │   ├── config/[machineId]/       # Edit configuration route
│   │   ├── +layout.svelte            # Main layout
│   │   ├── +layout.js                # Client-side layout load
│   │   ├── +layout.server.js         # Server-side environment injection
│   │   └── +page.svelte              # Home/create configuration page
│   ├── app.css                       # Global styles
│   └── app.html                      # HTML template
├── static/
│   └── favicon.png
├── dockerfile                        # Docker configuration
├── package.json
├── svelte.config.js
└── vite.config.js
```

## Docker

Build and run with Docker:

```bash
docker build -t config-frontend .
docker run -p 80:80 \
  -e CONFIG_API_BASE_URL=http://config-api-svc/api/v1 \
  -e CONFIG_UI_AUTH_TOKEN=your-secret-token \
  config-frontend
```

## API Endpoints Used

The application communicates with the following Configuration API endpoints:

- `GET /configurations` - Fetch existing configurations
- `GET /configurations/{id}/content` - Fetch full configuration details
- `POST /configurations` - Create new configuration
- `PUT /configurations/{id}` - Update existing configuration

## Usage

### Authentication
1. Navigate to the application URL
2. Enter the authentication token (set via `CONFIG_UI_AUTH_TOKEN`)
3. Access the configuration interface

### Creating a Configuration
1. Select "Create New Configuration" from the dropdown
2. Fill in Machine ID, Editor Name, and Field Scalar
3. Add sensor mappings (key-value pairs)
4. Click "Create Configuration"

### Editing a Configuration
1. Select an existing configuration from the dropdown
2. Modify the fields as needed
3. Click "Update Configuration"

### Deep Linking
Access specific configurations directly via URL:
```
/config/{machine_id}
```

## Form Fields

- **Machine ID**: Unique identifier for the machine (cannot be changed after creation)
- **Editor Name**: Name of the person editing the configuration
- **Field Scalar**: Numeric scaling factor applied to sensor values
- **Sensor Mappings**: Key-value pairs mapping sensor identifiers to display names
