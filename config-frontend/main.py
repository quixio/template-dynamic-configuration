import flet as ft


from configuration_svc import (
    fetch_existing_configs,
    fetch_full_configuration,
    create_machine_configuration,
    update_machine_configuration,
    get_existing_target_keys
)


def main(page: ft.Page):
    page.title = "Machine Configuration Form"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    
    # State variables
    current_config_id = None
    existing_configs = []

    machine_id = ft.TextField(label="Machine ID", width=400)
    editor_name = ft.TextField(label="Editor Name", width=400)
    field_scalar = ft.TextField(label="Field Scalar", width=400)

    def load_configuration(target_key):
        """Load configuration by target key"""
        nonlocal current_config_id
        
        try:
            # Find config by target key
            config = None
            for c in existing_configs:
                if 'metadata' in c and c['metadata'].get('target_key') == target_key:
                    config = c
                    break
            
            if not config:
                return
            
            current_config_id = config['id']
            full_config = fetch_full_configuration(current_config_id)
            
            if full_config:
                # Update form fields
                machine_id.value = full_config.get('machine_id', '')
                editor_name.value = full_config.get('editor_name', '')
                field_scalar.value = full_config.get('field_scalar', 1.0)

                # Update mapping
                mapping = full_config.get('mapping', {})
                
                # Clear existing mapping rows
                mapping_rows.clear()
                mapping_container.controls.clear()
                
                # Add rows for existing mapping
                if mapping:
                    for key, value in mapping.items():
                        add_mapping_row_with_values(key, value)
                else:
                    add_mapping_row()
                
                show_success(f"Loaded configuration: {target_key}")
                page.update()
        except Exception as e:
            show_error(str(e))
    
    def clear_form():
        """Clear all form fields"""
        nonlocal current_config_id
        current_config_id = None
        machine_id.value = ""
        editor_name.value = ""
        field_scalar.value = 1.0

        # Clear mapping
        mapping_rows.clear()
        mapping_container.controls.clear()
        add_mapping_row()
        
        page.update()
    
    def on_config_selection_change(e):
        """Handle configuration selection change"""
        selected = e.control.value
        
        if selected == "Create New Configuration":
            clear_form()
            # Update URL
            page.go("/")
        else:
            load_configuration(selected)
            # Update URL
            page.go(f"/config/{selected}")
    
    def handle_route_change(e):
        """Handle route changes"""
        route = e.route
        
        if route.startswith("/config/"):
            # Extract config name from route
            config_name = route.split("/config/")[1]
            
            # Set dropdown selection
            config_selector.value = config_name
            load_configuration(config_name)
        else:
            # Root route - create new
            config_selector.value = "Create New Configuration"
            clear_form()
    
    # Set up routing
    page.on_route_change = handle_route_change
    
    # Sensor mapping table
    mapping_rows = []
    mapping_container = ft.Column([])
    
    def add_mapping_row(key_val="", value_val=""):
        row_index = len(mapping_rows)
        key_field = ft.TextField(label=f"Key {row_index + 1}", width=200, value=key_val)
        value_field = ft.TextField(label=f"Value {row_index + 1}", width=200, value=value_val)
        
        remove_btn = ft.IconButton(
            ft.Icons.DELETE,
            on_click=lambda _: remove_mapping_row(row_container)
        )
        
        row_container = ft.Row([
            key_field,
            value_field,
            remove_btn
        ])
        
        # Store references to the fields
        row_container.key_field = key_field
        row_container.value_field = value_field
        
        mapping_rows.append(row_container)
        mapping_container.controls = mapping_rows[:]
        page.update()
    
    def add_mapping_row_with_values(key_val, value_val):
        add_mapping_row(key_val, value_val)
    
    def remove_mapping_row(row_to_remove):
        if len(mapping_rows) > 1:  # Keep at least one row
            mapping_rows.remove(row_to_remove)
            mapping_container.controls = mapping_rows[:]
            page.update()
    
    def submit_experiment(_):
        # Validate required fields
        if not machine_id.value:
            show_error("Machine ID is required")
            return
        if not editor_name.value:
            show_error("Editor Name is required")
            return
        
        # Build mapping from rows
        mapping = {}
        for row in mapping_rows:
            key_val = row.key_field.value
            value_val = row.value_field.value
            if key_val and value_val:
                mapping[key_val] = value_val
        
        # Check if this is an update or create
        is_update = current_config_id is not None

        try:
            if is_update:
                # Update existing configuration
                update_machine_configuration(
                    current_config_id,
                    machine_id.value,
                    editor_name.value,
                    field_scalar.value,
                    mapping,
                )
                show_success("Machine configuration updated successfully!")
            else:
                # For new configurations, check for duplicates
                existing_target_keys = get_existing_target_keys(existing_configs)
                
                if machine_id.value in existing_target_keys:
                    show_error(f"Configuration for machine '{machine_id.value}' already exists. Please choose a different machine ID or select the existing configuration to edit.")
                    return
                
                # Create new configuration
                create_machine_configuration(
                    machine_id.value,
                    editor_name.value,
                    field_scalar.value,
                    mapping,
                )
                show_success("Machine configuration created successfully!")
                
                # Navigate to the new configuration and refresh list
                page.go(f"/config/{machine_id.value}")
                refresh_config_selector()
        except Exception as e:
            show_error(str(e))
    
    def hide_banner():
        message_banner.visible = False
        page.update()
    
    def show_error(message):
        message_banner.bgcolor = ft.Colors.RED_100
        message_banner.content.controls[0] = ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED)
        message_banner.content.controls[1] = ft.Text(message, color=ft.Colors.RED, expand=True)
        message_banner.visible = True
        page.update()
    
    def show_success(message):
        message_banner.bgcolor = ft.Colors.GREEN_100
        message_banner.content.controls[0] = ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN)
        message_banner.content.controls[1] = ft.Text(message, color=ft.Colors.GREEN, expand=True)
        message_banner.visible = True
        page.update()

    def refresh_config_selector():
        """Refresh the configuration selector dropdown"""
        nonlocal existing_configs
        try:
            existing_configs = fetch_existing_configs()
            if not existing_configs:
                # A default/example config to get you started.
                create_machine_configuration(
                    machine_id="3D_PRINTER_2", 
                    editor_name="DEFAULT", 
                    scalar=1.0,
                    mapping={"T001": "sensor_1", "T002": "sensor_2"},
                )
                refresh_config_selector()
            
            # Create dropdown options
            config_options = [ft.dropdown.Option("Create New Configuration")]
            
            for config in existing_configs:
                if 'metadata' in config and 'target_key' in config['metadata']:
                    target_key = config['metadata']['target_key']
                    config_options.append(ft.dropdown.Option(target_key))
            
            config_selector.options = config_options
            page.update()
        except Exception as e:
            show_error(str(e))
    
    # UI Components
    message_banner = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED),
            ft.Text("", expand=True),
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                on_click=lambda _: hide_banner(),
                icon_size=16
            )
        ]),
        bgcolor=ft.Colors.RED_100,
        padding=10,
        border_radius=5,
        width=500,
        visible=False
    )
    
    # Configuration selector
    config_selector = ft.Dropdown(
        label="Select Configuration",
        width=400,
        on_change=on_config_selection_change,
        options=[ft.dropdown.Option("Create New Configuration")],
        value="Create New Configuration"
    )
    
    # Load existing configs and refresh selector
    refresh_config_selector()
    
    # Create initial mapping row
    add_mapping_row()
    
    submit_btn = ft.ElevatedButton(
        "Submit Machine Configuration",
        on_click=submit_experiment,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )
    
    # Layout
    page.add(
        ft.Container(
            content=ft.Text("Machine Configuration Form", style=ft.TextThemeStyle.HEADLINE_LARGE),
            margin=ft.margin.only(bottom=20)
        ),
        
        ft.Container(
            content=ft.Column([
                config_selector
            ]),
            bgcolor=ft.Colors.GREY_900,
            padding=20,
            border_radius=10
        ),
        
        ft.Container(margin=ft.margin.only(bottom=20)),
        
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("Machine Details", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                        margin=ft.margin.only(bottom=15)
                    ),
                    machine_id,
                    editor_name,
                    field_scalar,
                ]),
                bgcolor=ft.Colors.GREY_900,
                padding=20,
                border_radius=10,
                height=400
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Text("Machine Sensor Mapping", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                            ft.IconButton(
                                icon=ft.Icons.ADD,
                                on_click=lambda _: add_mapping_row(),
                                tooltip="Add mapping row"
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        margin=ft.margin.only(bottom=15)
                    ),
                    mapping_container
                ]),
                bgcolor=ft.Colors.GREY_900,
                padding=20,
                border_radius=10,
                height=400
            )
        ], spacing=20, alignment=ft.MainAxisAlignment.START),
        
        ft.Container(margin=ft.margin.only(bottom=20)),
        
        message_banner,
        submit_btn
    )
    
    # Handle initial route
    if page.route.startswith("/config/"):
        config_name = page.route.split("/config/")[1]
        config_selector.value = config_name
        load_configuration(config_name)


ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=80, host="0.0.0.0")