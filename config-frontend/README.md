# Experiment Configuration Form (Flet)

A modern Flet-based desktop/web application for creating and managing experiment configurations in the Configuration Management System.

![screenshot](screenshot.png)

## Overview

This service provides an enhanced alternative to the Streamlit form with better user experience, routing capabilities, and desktop application support. Built with Google's Flet framework, it offers native-like performance and responsive design.

## Features

- **Modern UI**: Clean, responsive interface with dark theme
- **Enhanced Routing**: URL-based navigation with deep linking support
- **Real-time Updates**: Dynamic configuration loading and form state management
- **Desktop/Web Support**: Runs as both desktop application and web service
- **Advanced Form Controls**: Rich UI components with better user interaction
- **Configuration Management**: Full CRUD operations for experiment configurations

## Architecture

The application is structured with:

- **main.py**: Main Flet application with UI components and routing
- **configuration_svc.py**: Service layer for Configuration API integration
- **storage/**: Local data storage for application state

## Form Features

### Configuration Selection
- Dropdown with existing configurations
- URL routing for direct configuration access
- Real-time configuration loading

### Form Fields
- **Experiment Name**: Text input with validation
- **Machine ID**: Unique identifier input
- **Test Engineer**: Engineer name input
- **Location**: Dropdown (Prague, Dresden, London)
- **Toner Material**: Material selection (ABS, PLA)
- **Price per kg**: Auto-calculated pricing (ABS: €22/kg, PLA: €18/kg)

### Sensor Mapping Interface
- Dynamic table with add/remove functionality
- Key-value pair configuration
- Visual feedback for mapping changes
- Icon-based row management

## API Integration

Integrates with Configuration API using the same format as the Streamlit version:

```json
{
  "metadata": {
    "type": "experiment-cfg",
    "target_key": "machine1",
    "valid_from": "2025-06-27T13:01:09.830Z",
    "category": "Test rig"
  },
  "content": {
    "experiment_name": "Test Experiment",
    "mapping": {"sensor1": "temperature"},
    "machine_id": "machine1",
    "test_engineer": "Engineer Name",
    "location": "Prague",
    "MATERIAL": "abs",
    "price_per_kg": 22.0
  }
}
```

## Environment Variables

- **CONFIG_API_BASE_URL**: Base URL of the Configuration API service

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export CONFIG_API_BASE_URL="http://localhost:8080/api/v1"

# Run as web application
python main.py

# Run as desktop application (requires Flet desktop)
flet main.py
```

### Docker Deployment

```bash
# Build Docker image
docker build -t machine-config-form .

# Run container
docker run -p 80:80 -e CONFIG_API_BASE_URL="http://api:8080/api/v1" machine-config-form
```

## Usage

### Web Application
1. Navigate to the deployed URL
2. Access specific configurations via `/config/{machine_id}` routes
3. Use the interface to create/edit configurations

### Desktop Application
1. Install Flet on your system
2. Run the application directly
3. Enjoy native desktop performance

## Advanced Features

### Routing System
- URL-based navigation: `/config/{machine_id}`
- Deep linking support for direct configuration access
- Browser back/forward button support

### State Management
- Persistent form state across navigation
- Configuration caching for better performance
- Error state recovery and validation

### UI Components
- Modern Material Design interface
- Responsive layout for different screen sizes
- Icon-based actions and visual feedback
- Success/error message banners

### Configuration Service
- Abstracted API communication layer
- Error handling and retry logic
- Configuration validation and transformation
- Duplicate detection for machine IDs

## Error Handling

Comprehensive error handling includes:
- API connectivity issues
- Form validation errors
- Duplicate configuration detection
- Network timeout recovery
- User-friendly error messages with dismissible banners

## Advantages over Streamlit Version

- **Better Performance**: Native application performance
- **Enhanced UX**: More responsive and interactive interface
- **Routing**: Proper URL routing and navigation
- **Desktop Support**: Can run as native desktop application
- **State Management**: Better handling of form state and navigation
- **Visual Design**: Modern Material Design components

## Technical Details

- **Framework**: Flet (Python-based Flutter wrapper)
- **Port**: 80 (configurable)
- **Host**: 0.0.0.0 (all interfaces)
- **View**: Web browser mode
- **Storage**: Local storage for temporary data