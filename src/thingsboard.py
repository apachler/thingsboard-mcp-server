from typing import Any, Optional, Dict, get_args

import fastmcp.server.server
import httpx
from fastmcp import FastMCP
import os
from dotenv import load_dotenv
import sys

load_dotenv()

mcp = FastMCP("ThingsBoard")

# Environment variables
MCP_SERVER_TRANSPORT = os.getenv("MCP_SERVER_TRANSPORT", "streamable-http")
THINGSBOARD_API_BASE = os.getenv("THINGSBOARD_API_BASE", None)
THINGSBOARD_USERNAME = os.getenv("THINGSBOARD_USERNAME", None)
THINGSBOARD_PASSWORD = os.getenv("THINGSBOARD_PASSWORD", None)

# Global variable to store the authentication token
auth_token: Optional[str] = None

# Type for permission request response
PermissionRequest = Dict[str, Any]


@mcp.tool()
async def acknowledge_alarm(alarm_id: str) -> Any:
    """Acknowledge an alarm.

    Args:
        alarm_id (str): Alarm ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"alarm/{alarm_id}/ack"
    response = await make_thingsboard_request(endpoint, method="POST")
    return await handle_permission_request(response)


@mcp.tool()
async def assign_alarm(alarmId: str, assigneeId: str) -> Any:
    """Assign/Reassign Alarm (assignAlarm)

    Args:
        alarmId (str): The alarm ID
        assigneeId (str): The assignee ID

    Returns:
        Any: JSON response
    """
    endpoint = f"alarm/{alarmId}/assign/{assigneeId}"
    params = None
    return await make_thingsboard_request(endpoint, method="post", params=params)


@mcp.tool()
async def clear_alarm(alarm_id: str) -> Any:
    """Clear an alarm.

    Args:
        alarm_id (str): Alarm ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"alarm/{alarm_id}/clear"
    response = await make_thingsboard_request(endpoint, method="POST")
    return await handle_permission_request(response)


@mcp.tool()
async def delete_alarm(alarm_id: str) -> Any:
    """Delete an alarm.

    Args:
        alarm_id (str): Alarm ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"alarm/{alarm_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def get_alarm_by_id(alarm_id: str) -> Any:
    """Get alarm by ID.

    Args:
        alarm_id (str): Alarm ID

    Returns:
        Any: JSON response with alarm details
    """
    endpoint = f"alarm/{alarm_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_alarm_comments(
    alarmId: str,
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Alarm comments (getAlarmComments)

    Args:
        alarmId (str): The alarm ID
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = f"alarm/{alarmId}/comment"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_alarm_info_by_id(alarmId: str) -> Any:
    """Get Alarm Info (getAlarmInfoById)

    Args:
        alarmId (str): The alarm ID

    Returns:
        Any: JSON response
    """
    endpoint = f"alarm/info/{alarmId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_alarms(
    entity_type: str,
    entity_id: str,
    search_status: Optional[str] = None,
    severity: Optional[str] = None,
    page: int = 0,
    page_size: int = 10,
) -> Any:
    """Get alarms for a specific entity.

    Args:
        entity_type (str): Entity type (DEVICE, ASSET, etc.)
        entity_id (str): Entity ID
        search_status (Optional[str]): Alarm status (ACTIVE, CLEARED, ACK, etc.)
        severity (Optional[str]): Alarm severity (CRITICAL, MAJOR, MINOR, WARNING, INDETERMINATE)
        page (int): Page number. Defaults to 0.
        page_size (int): Page size. Defaults to 10.

    Returns:
        Any: JSON response with alarms
    """
    endpoint = "alarm/{entity_type}/{entity_id}"
    params = {"page": page, "pageSize": page_size}

    if search_status:
        params["searchStatus"] = search_status
    if severity:
        params["severity"] = severity

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def create_asset(
    name: str,
    type: str,
    label: Optional[str] = None,
    additional_info: Optional[dict] = None,
) -> Any:
    """Create a new asset.

    Args:
        name (str): Name of the asset
        type (str): Type of the asset
        label (Optional[str]): Label of the asset
        additional_info (Optional[dict]): Additional info for the asset

    Returns:
        Any: JSON response with created asset details or a permission request
    """
    endpoint = "asset"
    data = {"name": name, "type": type}

    if label:
        data["label"] = label
    if additional_info:
        data["additionalInfo"] = additional_info

    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def delete_asset(asset_id: str) -> Any:
    """Delete an asset.

    Args:
        asset_id (str): The ID of the asset to delete.

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"asset/{asset_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def get_asset_attributes(asset_id: str) -> Any:
    """Get attributes for a specific asset.

    Args:
        asset_id (str): The ID of the asset.

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/ASSET/{asset_id}/values/attributes"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_asset_by_id(asset_id: str) -> Any:
    """Get asset details by asset ID.

    Args:
        asset_id (str): The ID of the asset.

    Returns:
        Any: JSON response with asset details
    """
    endpoint = f"asset/{asset_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_asset_by_name(asset_name: str) -> Any:
    """Get asset details by asset name.

    Args:
        asset_name (str): The name of the asset.

    Returns:
        Any: JSON response with asset details
    """
    endpoint = "tenant/assets"
    params = {"assetName": asset_name}
    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_tenant_assets(
    page: int = 0,
    page_size: int = 10,
    text_search: Optional[str] = None,
    sort_property: Optional[str] = None,
    sort_order: Optional[str] = None,
) -> Any:
    """Get a paginated list of assets for the tenant.

    Args:
        page (int): The page number to retrieve. Defaults to 0.
        page_size (int): The number of assets per page. Defaults to 10.
        text_search (Optional[str]): Text search parameter. Defaults to None.
        sort_property (Optional[str]): Property to sort by. Defaults to None.
        sort_order (Optional[str]): Sort order (ASC or DESC). Defaults to None.

    Returns:
        Any: JSON response with assets
    """
    endpoint = "tenant/assets"
    params = {"page": page, "pageSize": page_size}

    if text_search:
        params["textSearch"] = text_search
    if sort_property:
        params["sortProperty"] = sort_property
    if sort_order:
        params["sortOrder"] = sort_order

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def ack_alarm(alarmId: str) -> Any:
    """Acknowledge Alarm (ackAlarm)

    Args:
        alarmId (str): The alarm ID

    Returns:
        Any: JSON response
    """
    endpoint = f"alarm/{alarmId}/ack"
    params = None
    return await make_thingsboard_request(endpoint, method="post", params=params)


@mcp.tool()
async def save_asset_attributes(
    asset_id: str, attributes: dict, scope: str = "SERVER_SCOPE"
) -> Any:
    """Save attributes for a specific asset.

    Args:
        asset_id (str): The ID of the asset.
        attributes (dict): Attributes to save.
        scope (str): Scope of the attributes (SERVER_SCOPE, SHARED_SCOPE, CLIENT_SCOPE).

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"plugins/telemetry/ASSET/{asset_id}/{scope}"
    response = await make_thingsboard_request(
        endpoint, method="POST", json_data=attributes
    )
    return await handle_permission_request(response)


@mcp.tool()
async def update_asset(
    asset_id: str,
    name: Optional[str] = None,
    type: Optional[str] = None,
    label: Optional[str] = None,
    additional_info: Optional[dict] = None,
) -> Any:
    """Update an existing asset.

    Args:
        asset_id (str): The ID of the asset to update
        name (Optional[str]): New name for the asset
        type (Optional[str]): New type for the asset
        label (Optional[str]): New label for the asset
        additional_info (Optional[dict]): New additional info for the asset

    Returns:
        Any: JSON response with updated asset details or a permission request
    """
    # First get the current asset data
    current_asset = await get_asset_by_id(asset_id)

    if "error" in current_asset:
        return current_asset

    # Update only the fields that are provided
    data = current_asset

    if name:
        data["name"] = name
    if type:
        data["type"] = type
    if label:
        data["label"] = label
    if additional_info:
        if "additionalInfo" not in data:
            data["additionalInfo"] = {}
        data["additionalInfo"].update(additional_info)

    endpoint = "asset"
    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def assign_dashboard_to_customer(dashboard_id: str, customer_id: str) -> Any:
    """Assign dashboard to a customer.

    Args:
        dashboard_id (str): Dashboard ID
        customer_id (str): Customer ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"customer/{customer_id}/dashboard/{dashboard_id}"
    response = await make_thingsboard_request(endpoint, method="POST")
    return await handle_permission_request(response)


@mcp.tool()
async def delete_customer(customerId: str) -> Any:
    """Delete Customer

    Args:
        customerId (str): The customer ID

    Returns:
        Any: JSON response
    """
    endpoint = f"customer/{customerId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_customer_by_id(customerId: str) -> Any:
    """Get Customer by ID

    Args:
        customerId (str): The customer ID

    Returns:
        Any: JSON response
    """
    endpoint = f"customer/{customerId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_customers(
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Customers

    Args:
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        textSearch (Optional[str]): Text search parameter
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = "customers"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if textSearch:
        params["textSearch"] = textSearch
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_customer(json_data: dict) -> Any:
    """Save Customer

    Args:
        json_data (dict): The customer data

    Returns:
        Any: JSON response
    """
    endpoint = "customer"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def unassign_dashboard_from_customer(dashboard_id: str, customer_id: str) -> Any:
    """Unassign dashboard from a customer.

    Args:
        dashboard_id (str): Dashboard ID
        customer_id (str): Customer ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"customer/{customer_id}/dashboard/{dashboard_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def create_dashboard(
    title: str, configuration: dict, assigned_customers: Optional[list] = None
) -> Any:
    """Create a new dashboard.

    Args:
        title (str): Title of the dashboard
        configuration (dict): Dashboard configuration
        assigned_customers (Optional[list]): List of assigned customers

    Returns:
        Any: JSON response with created dashboard details or a permission request
    """
    endpoint = "dashboard"
    data = {"title": title, "configuration": configuration}

    if assigned_customers:
        data["assignedCustomers"] = assigned_customers

    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def delete_dashboard(dashboard_id: str) -> Any:
    """Delete a dashboard.

    Args:
        dashboard_id (str): The ID of the dashboard to delete.

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"dashboard/{dashboard_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def get_dashboard_by_id(dashboard_id: str) -> Any:
    """Get dashboard details by dashboard ID.

    Args:
        dashboard_id (str): The ID of the dashboard.

    Returns:
        Any: JSON response with dashboard details
    """
    endpoint = f"dashboard/{dashboard_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_dashboard_info_by_id(dashboard_id: str) -> Any:
    """Get dashboard info by dashboard ID.

    Args:
        dashboard_id (str): The ID of the dashboard.

    Returns:
        Any: JSON response with dashboard info
    """
    endpoint = f"dashboard/info/{dashboard_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_tenant_dashboards(
    page: int = 0, page_size: int = 10, text_search: Optional[str] = None
) -> Any:
    """Get a paginated list of dashboards for the tenant.

    Args:
        page (int): The page number to retrieve. Defaults to 0.
        page_size (int): The number of dashboards per page. Defaults to 10.
        text_search (Optional[str]): Text search parameter. Defaults to None.

    Returns:
        Any: JSON response with dashboards
    """
    endpoint = "tenant/dashboards"
    params = {"page": page, "pageSize": page_size}

    if text_search:
        params["textSearch"] = text_search

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def update_dashboard(
    dashboard_id: str,
    title: Optional[str] = None,
    configuration: Optional[dict] = None,
    assigned_customers: Optional[list] = None,
) -> Any:
    """Update an existing dashboard.

    Args:
        dashboard_id (str): The ID of the dashboard to update
        title (Optional[str]): New title for the dashboard
        configuration (Optional[dict]): New configuration for the dashboard
        assigned_customers (Optional[list]): New list of assigned customers

    Returns:
        Any: JSON response with updated dashboard details or a permission request
    """
    # First get the current dashboard data
    current_dashboard = await get_dashboard_by_id(dashboard_id)

    if "error" in current_dashboard:
        return current_dashboard

    # Update only the fields that are provided
    data = current_dashboard

    if title:
        data["title"] = title
    if configuration:
        data["configuration"] = configuration
    if assigned_customers:
        data["assignedCustomers"] = assigned_customers

    endpoint = "dashboard"
    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def create_device(
    name: str,
    type: str,
    label: Optional[str] = None,
    device_profile_id: Optional[str] = None,
    additional_info: Optional[dict] = None,
) -> Any:
    """Create a new device.

    Args:
        name (str): Name of the device
        type (str): Type of the device
        label (Optional[str]): Label of the device
        device_profile_id (Optional[str]): Device profile ID
        additional_info (Optional[dict]): Additional info for the device

    Returns:
        Any: JSON response with created device details or a permission request
    """
    endpoint = "device"
    data = {"name": name, "type": type}

    if label:
        data["label"] = label
    if device_profile_id:
        data["deviceProfileId"] = {"id": device_profile_id}
    if additional_info:
        data["additionalInfo"] = additional_info

    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def delete_device(device_id: str) -> Any:
    """Delete a device.

    Args:
        device_id (str): The ID of the device to delete.

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"device/{device_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def get_device_by_id(device_id: str) -> Any:
    """Get device details by device ID.

    Args:
        device_id (str): The ID of the device.

    Returns:
        Any: JSON response with device details
    """
    endpoint = f"device/{device_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_device_by_name(device_name: str) -> Any:
    """Get device details by device name.

    Args:
        device_name (str): The name of the device.

    Returns:
        Any: JSON response with device details
    """
    endpoint = f"tenant/devices"
    params = {"deviceName": device_name}
    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_device_credentials(device_id: str) -> Any:
    """Get credentials for a specific device.

    Args:
        device_id (str): The ID of the device.

    Returns:
        Any: JSON response with device credentials
    """
    endpoint = f"device/{device_id}/credentials"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def save_device_attributes(
    device_id: str, attributes: dict, scope: str = "SERVER_SCOPE"
) -> Any:
    """Save attributes for a specific device.

    Args:
        device_id (str): The ID of the device.
        attributes (dict): Attributes to save.
        scope (str): Scope of the attributes (SERVER_SCOPE, SHARED_SCOPE, CLIENT_SCOPE).

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"plugins/telemetry/{device_id}/{scope}"
    response = await make_thingsboard_request(
        endpoint, method="POST", json_data=attributes
    )
    return await handle_permission_request(response)


@mcp.tool()
async def update_device(
    device_id: str,
    name: Optional[str] = None,
    type: Optional[str] = None,
    label: Optional[str] = None,
    additional_info: Optional[dict] = None,
) -> Any:
    """Update an existing device.

    Args:
        device_id (str): The ID of the device to update
        name (Optional[str]): New name for the device
        type (Optional[str]): New type for the device
        label (Optional[str]): New label for the device
        additional_info (Optional[dict]): New additional info for the device

    Returns:
        Any: JSON response with updated device details or a permission request
    """
    # First get the current device data
    current_device = await get_device_by_id(device_id)

    if "error" in current_device:
        return current_device

    # Update only the fields that are provided
    data = current_device

    if name:
        data["name"] = name
    if type:
        data["type"] = type
    if label:
        data["label"] = label
    if additional_info:
        if "additionalInfo" not in data:
            data["additionalInfo"] = {}
        data["additionalInfo"].update(additional_info)

    endpoint = "device"
    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def delete_device_profile(deviceProfileId: str) -> Any:
    """Delete Device Profile

    Args:
        deviceProfileId (str): The device profile ID

    Returns:
        Any: JSON response
    """
    endpoint = f"deviceProfile/{deviceProfileId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_device_profile_by_id(deviceProfileId: str) -> Any:
    """Get Device Profile by ID

    Args:
        deviceProfileId (str): The device profile ID

    Returns:
        Any: JSON response
    """
    endpoint = f"deviceProfile/{deviceProfileId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_device_profiles(
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Device Profiles

    Args:
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        textSearch (Optional[str]): Text search parameter
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = "deviceProfiles"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if textSearch:
        params["textSearch"] = textSearch
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_device_profile(json_data: dict) -> Any:
    """Save Device Profile

    Args:
        json_data (dict): The device profile data

    Returns:
        Any: JSON response
    """
    endpoint = "deviceProfile"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def delete_entity(entityType: str, entityId: str) -> Any:
    """Delete Entity

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID

    Returns:
        Any: JSON response
    """
    endpoint = f"entity/{entityType}/{entityId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def delete_entity_attributes(
    entityType: str, entityId: str, scope: str, keys: str
) -> Any:
    """Delete Entity Attributes

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        scope (str): The scope of attributes (SERVER_SCOPE, SHARED_SCOPE, CLIENT_SCOPE)
        keys (str): Comma-separated list of keys to delete

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/{scope}"
    params = {"keys": keys}

    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def delete_entity_timeseries(
    entityType: str,
    entityId: str,
    keys: str,
    deleteAllDataForKeys: Optional[bool] = None,
    startTs: Optional[str] = None,
    endTs: Optional[str] = None,
    deleteLatest: Optional[bool] = None,
    rewriteLatestIfDeleted: Optional[bool] = None,
) -> Any:
    """Delete Entity Timeseries

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        keys (str): Comma-separated list of keys to delete
        deleteAllDataForKeys (Optional[bool]): If true, all data for specified keys will be deleted
        startTs (Optional[str]): Start timestamp in milliseconds (required if deleteAllDataForKeys is false)
        endTs (Optional[str]): End timestamp in milliseconds (required if deleteAllDataForKeys is false)
        deleteLatest (Optional[bool]): If true, latest values for specified keys will be deleted
        rewriteLatestIfDeleted (Optional[bool]): If true, latest value will be rewritten if it was removed

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/timeseries/delete"
    params = {"keys": keys}

    if deleteAllDataForKeys is not None:
        params["deleteAllDataForKeys"] = str(deleteAllDataForKeys).lower()

    if startTs is not None:
        params["startTs"] = startTs

    if endTs is not None:
        params["endTs"] = endTs

    if deleteLatest is not None:
        params["deleteLatest"] = str(deleteLatest).lower()

    if rewriteLatestIfDeleted is not None:
        params["rewriteLatestIfDeleted"] = str(rewriteLatestIfDeleted).lower()

    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_entity_by_id(entityType: str, entityId: str) -> Any:
    """Get Entity by ID

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID

    Returns:
        Any: JSON response
    """
    endpoint = f"entity/{entityType}/{entityId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_entity_latest_timeseries(
    entityType: str, entityId: str, keys: Optional[str] = None
) -> Any:
    """Get Entity Latest Timeseries

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        keys (Optional[str]): Comma-separated list of keys

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/values/timeseries"
    params = {}
    if keys:
        params["keys"] = keys
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_entity_timeseries(
    entityType: str,
    entityId: str,
    keys: str,
    startTs: str,
    endTs: str,
    interval: Optional[int] = None,
    limit: Optional[int] = None,
    agg: Optional[str] = None,
) -> Any:
    """Get Entity Timeseries

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        keys (str): Comma-separated list of keys
        startTs (str): Start timestamp in milliseconds
        endTs (str): End timestamp in milliseconds
        interval (Optional[int]): Aggregation interval in milliseconds
        limit (Optional[int]): Max values to return
        agg (Optional[str]): Aggregation function (MIN, MAX, AVG, SUM, COUNT, NONE)

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/values/timeseries"
    params = {"keys": keys, "startTs": startTs, "endTs": endTs}
    if interval:
        params["interval"] = interval
    if limit:
        params["limit"] = limit
    if agg:
        params["agg"] = agg
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def count_entities_by_query(json_data: dict) -> Any:
    """Count entities by query

    Args:
        json_data (dict): The query specification. Should contain entityFilter.

    Returns:
        Any: JSON response with entity count
    """
    endpoint = "entitiesQuery/count"
    return await make_thingsboard_request(endpoint, method="post", json_data=json_data)


@mcp.tool()
async def find_entities_by_query(json_data: dict) -> Any:
    """Find entities by query

    Args:
        json_data (dict): The query specification. Should contain entityFilter, pageLink, and other query parameters.

    Returns:
        Any: JSON response with found entities
    """
    endpoint = "entitiesQuery/find"
    return await make_thingsboard_request(endpoint, method="post", json_data=json_data)


@mcp.tool()
async def find_entity_keys_by_query(
    json_data: dict,
    timeseries: Optional[bool] = None,
    attributes: Optional[bool] = None,
    scope: Optional[str] = None,
) -> Any:
    """Find entity keys by query

    Args:
        json_data (dict): The query specification. Should contain entityFilter.
        timeseries (Optional[bool]): Whether to include timeseries keys
        attributes (Optional[bool]): Whether to include attribute keys
        scope (Optional[str]): Attribute scope (SERVER_SCOPE, SHARED_SCOPE, CLIENT_SCOPE)

    Returns:
        Any: JSON response with entity keys
    """
    endpoint = "entitiesQuery/find/keys"
    params = {}

    if timeseries is not None:
        params["timeseries"] = str(timeseries).lower()

    if attributes is not None:
        params["attributes"] = str(attributes).lower()

    if scope is not None:
        params["scope"] = scope

    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def save_entity_telemetry(
    entityType: str, entityId: str, scope: str, json_data: dict
) -> Any:
    """Save Entity Telemetry

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        scope (str): The scope of the telemetry
        json_data (dict): The telemetry data

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/timeseries/{scope}"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def create_entity_relation(
    from_id: str,
    from_type: str,
    relation_type: str,
    to_id: str,
    to_type: str,
    additional_info: Optional[dict] = None,
) -> Any:
    """Create entity relation.

    Args:
        from_id (str): From entity ID
        from_type (str): From entity type
        relation_type (str): Type of relation
        to_id (str): To entity ID
        to_type (str): To entity type
        additional_info (Optional[dict]): Additional info for the relation

    Returns:
        Any: JSON response
    """
    endpoint = "relation"
    data = {
        "from": {"entityType": from_type, "id": from_id},
        "type": relation_type,
        "to": {"entityType": to_type, "id": to_id},
    }

    if additional_info:
        data["additionalInfo"] = additional_info

    return await make_thingsboard_request(endpoint, method="POST", json_data=data)


@mcp.tool()
async def delete_entity_relation(
    from_id: str, from_type: str, relation_type: str, to_id: str, to_type: str
) -> Any:
    """Delete entity relation.

    Args:
        from_id (str): From entity ID
        from_type (str): From entity type
        relation_type (str): Type of relation
        to_id (str): To entity ID
        to_type (str): To entity type

    Returns:
        Any: JSON response
    """
    endpoint = "relation"
    params = {
        "fromId": from_id,
        "fromType": from_type,
        "relationType": relation_type,
        "toId": to_id,
        "toType": to_type,
    }

    return await make_thingsboard_request(endpoint, method="DELETE", params=params)


@mcp.tool()
async def find_entity_by_relation(
    from_id: str, from_type: str, relation_type: str, to_type: str
) -> Any:
    """Find entities by relation.

    Args:
        from_id (str): From entity ID
        from_type (str): From entity type
        relation_type (str): Type of relation
        to_type (str): To entity type

    Returns:
        Any: JSON response with entities
    """
    endpoint = f"relations/find"
    params = {
        "fromId": from_id,
        "fromType": from_type,
        "relationType": relation_type,
        "toType": to_type,
    }

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_entity_relation_info(
    from_id: str, from_type: str, relation_type: str, to_id: str, to_type: str
) -> Any:
    """Get entity relation info.

    Args:
        from_id (str): From entity ID
        from_type (str): From entity type
        relation_type (str): Type of relation
        to_id (str): To entity ID
        to_type (str): To entity type

    Returns:
        Any: JSON response with relation info
    """
    endpoint = f"relation"
    params = {
        "fromId": from_id,
        "fromType": from_type,
        "relationType": relation_type,
        "toId": to_id,
        "toType": to_type,
    }

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_entity_relations(
    entity_id: str,
    entity_type: str,
    relation_type: Optional[str] = None,
    direction: str = "FROM",
) -> Any:
    """Get entity relations.

    Args:
        entity_id (str): Entity ID
        entity_type (str): Entity type (DEVICE, ASSET, etc.)
        relation_type (Optional[str]): Type of relation. Defaults to None.
        direction (str): Direction of relation (FROM or TO). Defaults to "FROM".

    Returns:
        Any: JSON response with relations
    """
    endpoint = "relations"
    params = {
        "fromId": entity_id if direction == "FROM" else None,
        "fromType": entity_type if direction == "FROM" else None,
        "toId": entity_id if direction == "TO" else None,
        "toType": entity_type if direction == "TO" else None,
        "relationType": relation_type,
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_relations(
    fromId: Optional[str] = None,
    fromType: Optional[str] = None,
    toId: Optional[str] = None,
    toType: Optional[str] = None,
    relationType: Optional[str] = None,
) -> Any:
    """Get Relations

    Args:
        fromId (Optional[str]): From entity ID
        fromType (Optional[str]): From entity type
        toId (Optional[str]): To entity ID
        toType (Optional[str]): To entity type
        relationType (Optional[str]): Relation type

    Returns:
        Any: JSON response
    """
    endpoint = "relations"
    params = {}
    if fromId:
        params["fromId"] = fromId
    if fromType:
        params["fromType"] = fromType
    if toId:
        params["toId"] = toId
    if toType:
        params["toType"] = toType
    if relationType:
        params["relationType"] = relationType
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_relation(json_data: dict) -> Any:
    """Save Relation

    Args:
        json_data (dict): The relation data

    Returns:
        Any: JSON response
    """
    endpoint = "relation"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def delete_tenant(tenantId: str) -> Any:
    """Delete Tenant

    Args:
        tenantId (str): The tenant ID

    Returns:
        Any: JSON response
    """
    endpoint = f"tenant/{tenantId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_tenant_by_id(tenantId: str) -> Any:
    """Get Tenant by ID

    Args:
        tenantId (str): The tenant ID

    Returns:
        Any: JSON response
    """
    endpoint = f"tenant/{tenantId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_tenants(
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Tenants

    Args:
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        textSearch (Optional[str]): Text search parameter
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = "tenants"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if textSearch:
        params["textSearch"] = textSearch
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_tenant(json_data: dict) -> Any:
    """Save Tenant

    Args:
        json_data (dict): The tenant data

    Returns:
        Any: JSON response
    """
    endpoint = "tenant"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def delete_user(userId: str) -> Any:
    """Delete User

    Args:
        userId (str): The user ID

    Returns:
        Any: JSON response
    """
    endpoint = f"user/{userId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_user_by_id(userId: str) -> Any:
    """Get User by ID

    Args:
        userId (str): The user ID

    Returns:
        Any: JSON response
    """
    endpoint = f"user/{userId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_users(
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Users

    Args:
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        textSearch (Optional[str]): Text search parameter
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = "users"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if textSearch:
        params["textSearch"] = textSearch
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_user(json_data: dict, sendActivationMail: Optional[bool] = None) -> Any:
    """Save User

    Args:
        json_data (dict): The user data
        sendActivationMail (Optional[bool]): Whether to send activation email

    Returns:
        Any: JSON response
    """
    endpoint = "user"
    params = {}
    if sendActivationMail is not None:
        params["sendActivationMail"] = str(sendActivationMail).lower()
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def delete_rule_chain(ruleChainId: str) -> Any:
    """Delete Rule Chain

    Args:
        ruleChainId (str): Rule Chain ID

    Returns:
        Any: JSON response
    """
    endpoint = f"ruleChain/{ruleChainId}"
    return await make_thingsboard_request(endpoint, method="delete")


@mcp.tool()
async def get_rule_chain_by_id(ruleChainId: str) -> Any:
    """Get Rule Chain by ID

    Args:
        ruleChainId (str): Rule Chain ID

    Returns:
        Any: JSON response with rule chain details
    """
    endpoint = f"ruleChain/{ruleChainId}"
    return await make_thingsboard_request(endpoint, method="get")


@mcp.tool()
async def save_rule_chain(json_data: dict) -> Any:
    """Create or Update Rule Chain

    Args:
        json_data (dict): Rule chain data

    Returns:
        Any: JSON response with created/updated rule chain
    """
    endpoint = "ruleChain"
    return await make_thingsboard_request(endpoint, method="post", json_data=json_data)


@mcp.tool()
async def acknowledge_notification_request(notificationRequestId: str) -> Any:
    """Acknowledge Notification Request

    Args:
        notificationRequestId (str): Notification Request ID

    Returns:
        Any: JSON response
    """
    endpoint = f"notification/request/{notificationRequestId}/ack"
    return await make_thingsboard_request(endpoint, method="post")


@mcp.tool()
async def get_notification_delivery_methods() -> Any:
    """Get Notification Delivery Methods

    Returns:
        Any: JSON response with available delivery methods
    """
    endpoint = "notification/deliveryMethods"
    return await make_thingsboard_request(endpoint, method="get")


@mcp.tool()
async def get_notification_requests(
    pageSize: int,
    page: int,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Notification Requests

    Args:
        pageSize (int): Maximum amount of entities in a one page
        page (int): Page number (starts from 0)
        textSearch (Optional[str]): Text search
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response with notification requests
    """
    endpoint = "notification/requests"
    params = {"pageSize": pageSize, "page": page}

    if textSearch is not None:
        params["textSearch"] = textSearch

    if sortProperty is not None:
        params["sortProperty"] = sortProperty

    if sortOrder is not None:
        params["sortOrder"] = sortOrder

    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def execute_with_permission(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    json_data: Optional[dict] = None,
) -> Any:
    """Execute a non-GET request to ThingsBoard API after permission has been granted.

    This function should be called after the user has reviewed and approved a permission request.

    Args:
        method (str): HTTP method (POST, PUT, DELETE)
        endpoint (str): The API endpoint to call
        params (Optional[dict]): Query parameters for the request
        json_data (Optional[dict]): JSON data to send in the request body

    Returns:
        Any: JSON response from the API
    """
    return await make_thingsboard_request(
        endpoint, method, params, json_data, permission_granted=True
    )


async def handle_permission_request(response: Any) -> Any:
    """Helper function to handle permission request responses.

    This function checks if a response from make_thingsboard_request is a permission request
    and returns it accordingly.

    Args:
        response: The response from make_thingsboard_request

    Returns:
        The original response, whether it's a permission request or not
    """
    if isinstance(response, dict) and response.get("requires_permission"):
        return response

    return response


def get_auth_token(username: str, password: str) -> str:
    """Retrieve the authentication token."""
    try:
        data = {"username": username, "password": password}
        with httpx.Client() as client:
            response = client.post(f"{THINGSBOARD_API_BASE}/auth/login", json=data)
            response.raise_for_status()
            return response.json()["token"]
    except Exception as e:
        raise ValueError(f"Error getting token: {e}")


async def make_thingsboard_request(
    endpoint: str,
    method: str = "GET",
    params: Optional[dict] = None,
    json_data: Optional[dict] = None,
    permission_granted: bool = False,
) -> Any:
    """Execute a request to the ThingsBoard API.

    Args:
        endpoint (str): The API endpoint to call
        method (str): HTTP method (GET, POST, PUT, DELETE)
        params (Optional[dict]): Query parameters for the request
        json_data (Optional[dict]): JSON data to send in the request body
        permission_granted (bool): Whether permission has been granted for non-GET methods

    Returns:
        Any: JSON response from the API or a permission request
    """
    global auth_token

    # For GET requests, proceed normally
    if method == "GET":
        if not auth_token:
            auth_token = get_auth_token(THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD)

        url = f"{THINGSBOARD_API_BASE}/{endpoint}"
        headers = {"Authorization": f"Bearer {auth_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                if response.status_code == 204:  # No content
                    return {"success": True}
                return response.json()
            except httpx.HTTPStatusError as e:
                # If unauthorized, refresh the token and retry
                if e.response.status_code == 401:
                    auth_token = get_auth_token(
                        THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD
                    )
                    headers["Authorization"] = f"Bearer {auth_token}"
                    response = await client.get(url, headers=headers, params=params)
                    response.raise_for_status()
                    if response.status_code == 204:  # No content
                        return {"success": True}
                    return response.json()
                return {
                    "error": f"Unable to get data from ThingsBoard",
                    "details": str(e),
                }
            except Exception as e:
                return {
                    "error": f"Unable to get data from ThingsBoard",
                    "details": str(e),
                }

    # For non-GET methods, check if permission has been granted
    if not permission_granted:
        # Create a descriptive message about what the operation will do
        operation_descriptions = {
            "POST": "create or add new data",
            "PUT": "update existing data",
            "DELETE": "permanently remove data",
        }

        operation_description = operation_descriptions.get(
            method, f"perform a {method} operation"
        )

        # Include information about the endpoint and data being sent
        endpoint_info = f"endpoint: {endpoint}"
        data_info = ""
        if json_data:
            data_info = f", data: {json_data}"

        # Return a permission request instead of executing the operation
        return {
            "requires_permission": True,
            "method": method,
            "endpoint": endpoint,
            "params": params,
            "json_data": json_data,
            "message": f"This operation will {operation_description} in ThingsBoard ({endpoint_info}{data_info}). Do you want to proceed?",
        }

    # If permission has been granted, proceed with the non-GET request
    if not auth_token:
        auth_token = get_auth_token(THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD)

    url = f"{THINGSBOARD_API_BASE}/{endpoint}"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with httpx.AsyncClient() as client:
        try:
            if method == "POST":
                response = await client.post(
                    url, headers=headers, params=params, json=json_data
                )
            elif method == "PUT":
                response = await client.put(
                    url, headers=headers, params=params, json=json_data
                )
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}

            response.raise_for_status()
            if response.status_code == 204:  # No content
                return {"success": True}
            return response.json()
        except httpx.HTTPStatusError as e:
            # If unauthorized, refresh the token and retry
            if e.response.status_code == 401:
                auth_token = get_auth_token(THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD)
                headers["Authorization"] = f"Bearer {auth_token}"

                if method == "POST":
                    response = await client.post(
                        url, headers=headers, params=params, json=json_data
                    )
                elif method == "PUT":
                    response = await client.put(
                        url, headers=headers, params=params, json=json_data
                    )
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers, params=params)

                response.raise_for_status()
                if response.status_code == 204:  # No content
                    return {"success": True}
                return response.json()
            return {
                "error": f"Unable to {method.lower()} data from ThingsBoard",
                "details": str(e),
            }
        except Exception as e:
            return {
                "error": f"Unable to {method.lower()} data from ThingsBoard",
                "details": str(e),
            }


@mcp.tool()
async def execute_with_permission(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    json_data: Optional[dict] = None,
) -> Any:
    """Execute a non-GET request to ThingsBoard API after permission has been granted.

    This function should be called after the user has reviewed and approved a permission request.

    Args:
        method (str): HTTP method (POST, PUT, DELETE)
        endpoint (str): The API endpoint to call
        params (Optional[dict]): Query parameters for the request
        json_data (Optional[dict]): JSON data to send in the request body

    Returns:
        Any: JSON response from the API
    """
    return await make_thingsboard_request(
        endpoint, method, params, json_data, permission_granted=True
    )


async def handle_permission_request(response: Any) -> Any:
    """Helper function to handle permission request responses.

    This function checks if a response from make_thingsboard_request is a permission request
    and returns it accordingly.

    Args:
        response: The response from make_thingsboard_request

    Returns:
        The original response, whether it's a permission request or not
    """
    if isinstance(response, dict) and response.get("requires_permission"):
        return response

    return response


def get_auth_token(username: str, password: str) -> str:
    """Retrieve the authentication token."""
    try:
        data = {"username": username, "password": password}
        with httpx.Client() as client:
            response = client.post(f"{THINGSBOARD_API_BASE}/auth/login", json=data)
            response.raise_for_status()
            return response.json()["token"]
    except Exception as e:
        raise ValueError(f"Error getting token: {e}")


async def make_thingsboard_request(
    endpoint: str,
    method: str = "GET",
    params: Optional[dict] = None,
    json_data: Optional[dict] = None,
    permission_granted: bool = False,
) -> Any:
    """Execute a request to the ThingsBoard API.

    Args:
        endpoint (str): The API endpoint to call
        method (str): HTTP method (GET, POST, PUT, DELETE)
        params (Optional[dict]): Query parameters for the request
        json_data (Optional[dict]): JSON data to send in the request body
        permission_granted (bool): Whether permission has been granted for non-GET methods

    Returns:
        Any: JSON response from the API or a permission request
    """
    global auth_token

    # For GET requests, proceed normally
    if method == "GET":
        if not auth_token:
            auth_token = get_auth_token(THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD)

        url = f"{THINGSBOARD_API_BASE}/{endpoint}"
        headers = {"Authorization": f"Bearer {auth_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                if response.status_code == 204:  # No content
                    return {"success": True}
                return response.json()
            except httpx.HTTPStatusError as e:
                # If unauthorized, refresh the token and retry
                if e.response.status_code == 401:
                    auth_token = get_auth_token(
                        THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD
                    )
                    headers["Authorization"] = f"Bearer {auth_token}"
                    response = await client.get(url, headers=headers, params=params)
                    response.raise_for_status()
                    if response.status_code == 204:  # No content
                        return {"success": True}
                    return response.json()
                return {
                    "error": f"Unable to get data from ThingsBoard",
                    "details": str(e),
                }
            except Exception as e:
                return {
                    "error": f"Unable to get data from ThingsBoard",
                    "details": str(e),
                }

    # For non-GET methods, check if permission has been granted
    if not permission_granted:
        # Create a descriptive message about what the operation will do
        operation_descriptions = {
            "POST": "create or add new data",
            "PUT": "update existing data",
            "DELETE": "permanently remove data",
        }

        operation_description = operation_descriptions.get(
            method, f"perform a {method} operation"
        )

        # Include information about the endpoint and data being sent
        endpoint_info = f"endpoint: {endpoint}"
        data_info = ""
        if json_data:
            data_info = f", data: {json_data}"

        # Return a permission request instead of executing the operation
        return {
            "requires_permission": True,
            "method": method,
            "endpoint": endpoint,
            "params": params,
            "json_data": json_data,
            "message": f"This operation will {operation_description} in ThingsBoard ({endpoint_info}{data_info}). Do you want to proceed?",
        }

    # If permission has been granted, proceed with the non-GET request
    if not auth_token:
        auth_token = get_auth_token(THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD)

    url = f"{THINGSBOARD_API_BASE}/{endpoint}"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with httpx.AsyncClient() as client:
        try:
            if method == "POST":
                response = await client.post(
                    url, headers=headers, params=params, json=json_data
                )
            elif method == "PUT":
                response = await client.put(
                    url, headers=headers, params=params, json=json_data
                )
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}

            response.raise_for_status()
            if response.status_code == 204:  # No content
                return {"success": True}
            return response.json()
        except httpx.HTTPStatusError as e:
            # If unauthorized, refresh the token and retry
            if e.response.status_code == 401:
                auth_token = get_auth_token(THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD)
                headers["Authorization"] = f"Bearer {auth_token}"

                if method == "POST":
                    response = await client.post(
                        url, headers=headers, params=params, json=json_data
                    )
                elif method == "PUT":
                    response = await client.put(
                        url, headers=headers, params=params, json=json_data
                    )
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers, params=params)

                response.raise_for_status()
                if response.status_code == 204:  # No content
                    return {"success": True}
                return response.json()
            return {
                "error": f"Unable to {method.lower()} data from ThingsBoard",
                "details": str(e),
            }
        except Exception as e:
            return {
                "error": f"Unable to {method.lower()} data from ThingsBoard",
                "details": str(e),
            }


@mcp.tool()
async def get_device_by_id(device_id: str) -> Any:
    """Get device details by device ID.

    Args:
        device_id (str): The ID of the device.

    Returns:
        Any: JSON response with device details
    """
    endpoint = f"device/{device_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_device_by_name(device_name: str) -> Any:
    """Get device details by device name.

    Args:
        device_name (str): The name of the device.

    Returns:
        Any: JSON response with device details
    """
    endpoint = f"tenant/devices"
    params = {"deviceName": device_name}
    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def create_device(
    name: str,
    type: str,
    label: Optional[str] = None,
    device_profile_id: Optional[str] = None,
    additional_info: Optional[dict] = None,
) -> Any:
    """Create a new device.

    Args:
        name (str): Name of the device
        type (str): Type of the device
        label (Optional[str]): Label of the device
        device_profile_id (Optional[str]): Device profile ID
        additional_info (Optional[dict]): Additional info for the device

    Returns:
        Any: JSON response with created device details or a permission request
    """
    endpoint = "device"
    data = {"name": name, "type": type}

    if label:
        data["label"] = label
    if device_profile_id:
        data["deviceProfileId"] = {"id": device_profile_id}
    if additional_info:
        data["additionalInfo"] = additional_info

    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def delete_device(device_id: str) -> Any:
    """Delete a device.

    Args:
        device_id (str): The ID of the device to delete.

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"device/{device_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def update_device(
    device_id: str,
    name: Optional[str] = None,
    type: Optional[str] = None,
    label: Optional[str] = None,
    additional_info: Optional[dict] = None,
) -> Any:
    """Update an existing device.

    Args:
        device_id (str): The ID of the device to update
        name (Optional[str]): New name for the device
        type (Optional[str]): New type for the device
        label (Optional[str]): New label for the device
        additional_info (Optional[dict]): New additional info for the device

    Returns:
        Any: JSON response with updated device details or a permission request
    """
    # First get the current device data
    current_device = await get_device_by_id(device_id)

    if "error" in current_device:
        return current_device

    # Update only the fields that are provided
    data = current_device

    if name:
        data["name"] = name
    if type:
        data["type"] = type
    if label:
        data["label"] = label
    if additional_info:
        if "additionalInfo" not in data:
            data["additionalInfo"] = {}
        data["additionalInfo"].update(additional_info)

    endpoint = "device"
    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def get_device_credentials(device_id: str) -> Any:
    """Get credentials for a specific device.

    Args:
        device_id (str): The ID of the device.

    Returns:
        Any: JSON response with device credentials
    """
    endpoint = f"device/{device_id}/credentials"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def save_device_attributes(
    device_id: str, attributes: dict, scope: str = "SERVER_SCOPE"
) -> Any:
    """Save attributes for a specific device.

    Args:
        device_id (str): The ID of the device.
        attributes (dict): Attributes to save.
        scope (str): Scope of the attributes (SERVER_SCOPE, SHARED_SCOPE, CLIENT_SCOPE).

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"plugins/telemetry/{device_id}/{scope}"
    response = await make_thingsboard_request(
        endpoint, method="POST", json_data=attributes
    )
    return await handle_permission_request(response)


@mcp.tool()
async def get_tenant_assets(
    page: int = 0,
    page_size: int = 10,
    text_search: Optional[str] = None,
    sort_property: Optional[str] = None,
    sort_order: Optional[str] = None,
) -> Any:
    """Get a paginated list of assets for the tenant.

    Args:
        page (int): The page number to retrieve. Defaults to 0.
        page_size (int): The number of assets per page. Defaults to 10.
        text_search (Optional[str]): Text search parameter. Defaults to None.
        sort_property (Optional[str]): Property to sort by. Defaults to None.
        sort_order (Optional[str]): Sort order (ASC or DESC). Defaults to None.

    Returns:
        Any: JSON response with assets
    """
    endpoint = "tenant/assets"
    params = {"page": page, "pageSize": page_size}

    if text_search:
        params["textSearch"] = text_search
    if sort_property:
        params["sortProperty"] = sort_property
    if sort_order:
        params["sortOrder"] = sort_order

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_asset_by_id(asset_id: str) -> Any:
    """Get asset details by asset ID.

    Args:
        asset_id (str): The ID of the asset.

    Returns:
        Any: JSON response with asset details
    """
    endpoint = f"asset/{asset_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_asset_by_name(asset_name: str) -> Any:
    """Get asset details by asset name.

    Args:
        asset_name (str): The name of the asset.

    Returns:
        Any: JSON response with asset details
    """
    endpoint = "tenant/assets"
    params = {"assetName": asset_name}
    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def create_asset(
    name: str,
    type: str,
    label: Optional[str] = None,
    additional_info: Optional[dict] = None,
) -> Any:
    """Create a new asset.

    Args:
        name (str): Name of the asset
        type (str): Type of the asset
        label (Optional[str]): Label of the asset
        additional_info (Optional[dict]): Additional info for the asset

    Returns:
        Any: JSON response with created asset details or a permission request
    """
    endpoint = "asset"
    data = {"name": name, "type": type}

    if label:
        data["label"] = label
    if additional_info:
        data["additionalInfo"] = additional_info

    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def delete_asset(asset_id: str) -> Any:
    """Delete an asset.

    Args:
        asset_id (str): The ID of the asset to delete.

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"asset/{asset_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def update_asset(
    asset_id: str,
    name: Optional[str] = None,
    type: Optional[str] = None,
    label: Optional[str] = None,
    additional_info: Optional[dict] = None,
) -> Any:
    """Update an existing asset.

    Args:
        asset_id (str): The ID of the asset to update
        name (Optional[str]): New name for the asset
        type (Optional[str]): New type for the asset
        label (Optional[str]): New label for the asset
        additional_info (Optional[dict]): New additional info for the asset

    Returns:
        Any: JSON response with updated asset details or a permission request
    """
    # First get the current asset data
    current_asset = await get_asset_by_id(asset_id)

    if "error" in current_asset:
        return current_asset

    # Update only the fields that are provided
    data = current_asset

    if name:
        data["name"] = name
    if type:
        data["type"] = type
    if label:
        data["label"] = label
    if additional_info:
        if "additionalInfo" not in data:
            data["additionalInfo"] = {}
        data["additionalInfo"].update(additional_info)

    endpoint = "asset"
    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def get_asset_attributes(asset_id: str) -> Any:
    """Get attributes for a specific asset.

    Args:
        asset_id (str): The ID of the asset.

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/ASSET/{asset_id}/values/attributes"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def save_asset_attributes(
    asset_id: str, attributes: dict, scope: str = "SERVER_SCOPE"
) -> Any:
    """Save attributes for a specific asset.

    Args:
        asset_id (str): The ID of the asset.
        attributes (dict): Attributes to save.
        scope (str): Scope of the attributes (SERVER_SCOPE, SHARED_SCOPE, CLIENT_SCOPE).

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"plugins/telemetry/ASSET/{asset_id}/{scope}"
    response = await make_thingsboard_request(
        endpoint, method="POST", json_data=attributes
    )
    return await handle_permission_request(response)


@mcp.tool()
async def get_alarms(
    entity_type: str,
    entity_id: str,
    search_status: Optional[str] = None,
    severity: Optional[str] = None,
    page: int = 0,
    page_size: int = 10,
) -> Any:
    """Get alarms for a specific entity.

    Args:
        entity_type (str): Entity type (DEVICE, ASSET, etc.)
        entity_id (str): Entity ID
        search_status (Optional[str]): Alarm status (ACTIVE, CLEARED, ACK, etc.)
        severity (Optional[str]): Alarm severity (CRITICAL, MAJOR, MINOR, WARNING, INDETERMINATE)
        page (int): Page number. Defaults to 0.
        page_size (int): Page size. Defaults to 10.

    Returns:
        Any: JSON response with alarms
    """
    endpoint = "alarm/{entity_type}/{entity_id}"
    params = {"page": page, "pageSize": page_size}

    if search_status:
        params["searchStatus"] = search_status
    if severity:
        params["severity"] = severity

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_alarm_by_id(alarm_id: str) -> Any:
    """Get alarm by ID.

    Args:
        alarm_id (str): Alarm ID

    Returns:
        Any: JSON response with alarm details
    """
    endpoint = f"alarm/{alarm_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def acknowledge_alarm(alarm_id: str) -> Any:
    """Acknowledge an alarm.

    Args:
        alarm_id (str): Alarm ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"alarm/{alarm_id}/ack"
    response = await make_thingsboard_request(endpoint, method="POST")
    return await handle_permission_request(response)


@mcp.tool()
async def clear_alarm(alarm_id: str) -> Any:
    """Clear an alarm.

    Args:
        alarm_id (str): Alarm ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"alarm/{alarm_id}/clear"
    response = await make_thingsboard_request(endpoint, method="POST")
    return await handle_permission_request(response)


@mcp.tool()
async def delete_alarm(alarm_id: str) -> Any:
    """Delete an alarm.

    Args:
        alarm_id (str): Alarm ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"alarm/{alarm_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def get_tenant_dashboards(
    page: int = 0, page_size: int = 10, text_search: Optional[str] = None
) -> Any:
    """Get a paginated list of dashboards for the tenant.

    Args:
        page (int): The page number to retrieve. Defaults to 0.
        page_size (int): The number of dashboards per page. Defaults to 10.
        text_search (Optional[str]): Text search parameter. Defaults to None.

    Returns:
        Any: JSON response with dashboards
    """
    endpoint = "tenant/dashboards"
    params = {"page": page, "pageSize": page_size}

    if text_search:
        params["textSearch"] = text_search

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_dashboard_by_id(dashboard_id: str) -> Any:
    """Get dashboard details by dashboard ID.

    Args:
        dashboard_id (str): The ID of the dashboard.

    Returns:
        Any: JSON response with dashboard details
    """
    endpoint = f"dashboard/{dashboard_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def get_dashboard_info_by_id(dashboard_id: str) -> Any:
    """Get dashboard info by dashboard ID.

    Args:
        dashboard_id (str): The ID of the dashboard.

    Returns:
        Any: JSON response with dashboard info
    """
    endpoint = f"dashboard/info/{dashboard_id}"
    return await make_thingsboard_request(endpoint)


@mcp.tool()
async def create_dashboard(
    title: str, configuration: dict, assigned_customers: Optional[list] = None
) -> Any:
    """Create a new dashboard.

    Args:
        title (str): Title of the dashboard
        configuration (dict): Dashboard configuration
        assigned_customers (Optional[list]): List of assigned customers

    Returns:
        Any: JSON response with created dashboard details or a permission request
    """
    endpoint = "dashboard"
    data = {"title": title, "configuration": configuration}

    if assigned_customers:
        data["assignedCustomers"] = assigned_customers

    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def update_dashboard(
    dashboard_id: str,
    title: Optional[str] = None,
    configuration: Optional[dict] = None,
    assigned_customers: Optional[list] = None,
) -> Any:
    """Update an existing dashboard.

    Args:
        dashboard_id (str): The ID of the dashboard to update
        title (Optional[str]): New title for the dashboard
        configuration (Optional[dict]): New configuration for the dashboard
        assigned_customers (Optional[list]): New list of assigned customers

    Returns:
        Any: JSON response with updated dashboard details or a permission request
    """
    # First get the current dashboard data
    current_dashboard = await get_dashboard_by_id(dashboard_id)

    if "error" in current_dashboard:
        return current_dashboard

    # Update only the fields that are provided
    data = current_dashboard

    if title:
        data["title"] = title
    if configuration:
        data["configuration"] = configuration
    if assigned_customers:
        data["assignedCustomers"] = assigned_customers

    endpoint = "dashboard"
    response = await make_thingsboard_request(endpoint, method="POST", json_data=data)
    return await handle_permission_request(response)


@mcp.tool()
async def delete_dashboard(dashboard_id: str) -> Any:
    """Delete a dashboard.

    Args:
        dashboard_id (str): The ID of the dashboard to delete.

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"dashboard/{dashboard_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def assign_dashboard_to_customer(dashboard_id: str, customer_id: str) -> Any:
    """Assign dashboard to a customer.

    Args:
        dashboard_id (str): Dashboard ID
        customer_id (str): Customer ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"customer/{customer_id}/dashboard/{dashboard_id}"
    response = await make_thingsboard_request(endpoint, method="POST")
    return await handle_permission_request(response)


@mcp.tool()
async def unassign_dashboard_from_customer(dashboard_id: str, customer_id: str) -> Any:
    """Unassign dashboard from a customer.

    Args:
        dashboard_id (str): Dashboard ID
        customer_id (str): Customer ID

    Returns:
        Any: JSON response or a permission request
    """
    endpoint = f"customer/{customer_id}/dashboard/{dashboard_id}"
    response = await make_thingsboard_request(endpoint, method="DELETE")
    return await handle_permission_request(response)


@mcp.tool()
async def get_entity_relations(
    entity_id: str,
    entity_type: str,
    relation_type: Optional[str] = None,
    direction: str = "FROM",
) -> Any:
    """Get entity relations.

    Args:
        entity_id (str): Entity ID
        entity_type (str): Entity type (DEVICE, ASSET, etc.)
        relation_type (Optional[str]): Type of relation. Defaults to None.
        direction (str): Direction of relation (FROM or TO). Defaults to "FROM".

    Returns:
        Any: JSON response with relations
    """
    endpoint = "relations"
    params = {
        "fromId": entity_id if direction == "FROM" else None,
        "fromType": entity_type if direction == "FROM" else None,
        "toId": entity_id if direction == "TO" else None,
        "toType": entity_type if direction == "TO" else None,
        "relationType": relation_type,
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_entity_relation_info(
    from_id: str, from_type: str, relation_type: str, to_id: str, to_type: str
) -> Any:
    """Get entity relation info.

    Args:
        from_id (str): From entity ID
        from_type (str): From entity type
        relation_type (str): Type of relation
        to_id (str): To entity ID
        to_type (str): To entity type

    Returns:
        Any: JSON response with relation info
    """
    endpoint = f"relation"
    params = {
        "fromId": from_id,
        "fromType": from_type,
        "relationType": relation_type,
        "toId": to_id,
        "toType": to_type,
    }

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def create_entity_relation(
    from_id: str,
    from_type: str,
    relation_type: str,
    to_id: str,
    to_type: str,
    additional_info: Optional[dict] = None,
) -> Any:
    """Create entity relation.

    Args:
        from_id (str): From entity ID
        from_type (str): From entity type
        relation_type (str): Type of relation
        to_id (str): To entity ID
        to_type (str): To entity type
        additional_info (Optional[dict]): Additional info for the relation

    Returns:
        Any: JSON response
    """
    endpoint = "relation"
    data = {
        "from": {"entityType": from_type, "id": from_id},
        "type": relation_type,
        "to": {"entityType": to_type, "id": to_id},
    }

    if additional_info:
        data["additionalInfo"] = additional_info

    return await make_thingsboard_request(endpoint, method="POST", json_data=data)


@mcp.tool()
async def delete_entity_relation(
    from_id: str, from_type: str, relation_type: str, to_id: str, to_type: str
) -> Any:
    """Delete entity relation.

    Args:
        from_id (str): From entity ID
        from_type (str): From entity type
        relation_type (str): Type of relation
        to_id (str): To entity ID
        to_type (str): To entity type

    Returns:
        Any: JSON response
    """
    endpoint = "relation"
    params = {
        "fromId": from_id,
        "fromType": from_type,
        "relationType": relation_type,
        "toId": to_id,
        "toType": to_type,
    }

    return await make_thingsboard_request(endpoint, method="DELETE", params=params)


@mcp.tool()
async def find_entity_by_relation(
    from_id: str, from_type: str, relation_type: str, to_type: str
) -> Any:
    """Find entities by relation.

    Args:
        from_id (str): From entity ID
        from_type (str): From entity type
        relation_type (str): Type of relation
        to_type (str): To entity type

    Returns:
        Any: JSON response with entities
    """
    endpoint = f"relations/find"
    params = {
        "fromId": from_id,
        "fromType": from_type,
        "relationType": relation_type,
        "toType": to_type,
    }

    return await make_thingsboard_request(endpoint, params=params)


@mcp.tool()
async def get_relations(
    fromId: Optional[str] = None,
    fromType: Optional[str] = None,
    toId: Optional[str] = None,
    toType: Optional[str] = None,
    relationType: Optional[str] = None,
) -> Any:
    """Get Relations

    Args:
        fromId (Optional[str]): From entity ID
        fromType (Optional[str]): From entity type
        toId (Optional[str]): To entity ID
        toType (Optional[str]): To entity type
        relationType (Optional[str]): Relation type

    Returns:
        Any: JSON response
    """
    endpoint = "relations"
    params = {}
    if fromId:
        params["fromId"] = fromId
    if fromType:
        params["fromType"] = fromType
    if toId:
        params["toId"] = toId
    if toType:
        params["toType"] = toType
    if relationType:
        params["relationType"] = relationType
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_relation(json_data: dict) -> Any:
    """Save Relation

    Args:
        json_data (dict): The relation data

    Returns:
        Any: JSON response
    """
    endpoint = "relation"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def ack_alarm(alarmId: str) -> Any:
    """Acknowledge Alarm (ackAlarm)

    Args:
        alarmId (str): The alarm ID

    Returns:
        Any: JSON response
    """
    endpoint = f"alarm/{alarmId}/ack"
    params = None
    return await make_thingsboard_request(endpoint, method="post", params=params)


@mcp.tool()
async def assign_alarm(alarmId: str, assigneeId: str) -> Any:
    """Assign/Reassign Alarm (assignAlarm)

    Args:
        alarmId (str): The alarm ID
        assigneeId (str): The assignee ID

    Returns:
        Any: JSON response
    """
    endpoint = f"alarm/{alarmId}/assign/{assigneeId}"
    params = None
    return await make_thingsboard_request(endpoint, method="post", params=params)


@mcp.tool()
async def get_alarm_comments(
    alarmId: str,
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Alarm comments (getAlarmComments)

    Args:
        alarmId (str): The alarm ID
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = f"alarm/{alarmId}/comment"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_alarm_info_by_id(alarmId: str) -> Any:
    """Get Alarm Info (getAlarmInfoById)

    Args:
        alarmId (str): The alarm ID

    Returns:
        Any: JSON response
    """
    endpoint = f"alarm/info/{alarmId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_device_profile_by_id(deviceProfileId: str) -> Any:
    """Get Device Profile by ID

    Args:
        deviceProfileId (str): The device profile ID

    Returns:
        Any: JSON response
    """
    endpoint = f"deviceProfile/{deviceProfileId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_device_profiles(
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Device Profiles

    Args:
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        textSearch (Optional[str]): Text search parameter
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = "deviceProfiles"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if textSearch:
        params["textSearch"] = textSearch
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_device_profile(json_data: dict) -> Any:
    """Save Device Profile

    Args:
        json_data (dict): The device profile data

    Returns:
        Any: JSON response
    """
    endpoint = "deviceProfile"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def delete_device_profile(deviceProfileId: str) -> Any:
    """Delete Device Profile

    Args:
        deviceProfileId (str): The device profile ID

    Returns:
        Any: JSON response
    """
    endpoint = f"deviceProfile/{deviceProfileId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_customer_by_id(customerId: str) -> Any:
    """Get Customer by ID

    Args:
        customerId (str): The customer ID

    Returns:
        Any: JSON response
    """
    endpoint = f"customer/{customerId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_customers(
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Customers

    Args:
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        textSearch (Optional[str]): Text search parameter
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = "customers"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if textSearch:
        params["textSearch"] = textSearch
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_customer(json_data: dict) -> Any:
    """Save Customer

    Args:
        json_data (dict): The customer data

    Returns:
        Any: JSON response
    """
    endpoint = "customer"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def delete_customer(customerId: str) -> Any:
    """Delete Customer

    Args:
        customerId (str): The customer ID

    Returns:
        Any: JSON response
    """
    endpoint = f"customer/{customerId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_user_by_id(userId: str) -> Any:
    """Get User by ID

    Args:
        userId (str): The user ID

    Returns:
        Any: JSON response
    """
    endpoint = f"user/{userId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_users(
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Users

    Args:
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        textSearch (Optional[str]): Text search parameter
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = "users"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if textSearch:
        params["textSearch"] = textSearch
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_user(json_data: dict, sendActivationMail: Optional[bool] = None) -> Any:
    """Save User

    Args:
        json_data (dict): The user data
        sendActivationMail (Optional[bool]): Whether to send activation email

    Returns:
        Any: JSON response
    """
    endpoint = "user"
    params = {}
    if sendActivationMail is not None:
        params["sendActivationMail"] = str(sendActivationMail).lower()
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def delete_user(userId: str) -> Any:
    """Delete User

    Args:
        userId (str): The user ID

    Returns:
        Any: JSON response
    """
    endpoint = f"user/{userId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_tenant_by_id(tenantId: str) -> Any:
    """Get Tenant by ID

    Args:
        tenantId (str): The tenant ID

    Returns:
        Any: JSON response
    """
    endpoint = f"tenant/{tenantId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_tenants(
    pageSize: Optional[int] = None,
    page: Optional[int] = None,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Tenants

    Args:
        pageSize (Optional[int]): The page size
        page (Optional[int]): The page number
        textSearch (Optional[str]): Text search parameter
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response
    """
    endpoint = "tenants"
    params = {}
    if pageSize:
        params["pageSize"] = pageSize
    if page:
        params["page"] = page
    if textSearch:
        params["textSearch"] = textSearch
    if sortProperty:
        params["sortProperty"] = sortProperty
    if sortOrder:
        params["sortOrder"] = sortOrder
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def save_tenant(json_data: dict) -> Any:
    """Save Tenant

    Args:
        json_data (dict): The tenant data

    Returns:
        Any: JSON response
    """
    endpoint = "tenant"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def delete_tenant(tenantId: str) -> Any:
    """Delete Tenant

    Args:
        tenantId (str): The tenant ID

    Returns:
        Any: JSON response
    """
    endpoint = f"tenant/{tenantId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_rule_chain_by_id(ruleChainId: str) -> Any:
    """Get Rule Chain by ID

    Args:
        ruleChainId (str): Rule Chain ID

    Returns:
        Any: JSON response with rule chain details
    """
    endpoint = f"ruleChain/{ruleChainId}"
    return await make_thingsboard_request(endpoint, method="get")


@mcp.tool()
async def save_rule_chain(json_data: dict) -> Any:
    """Create or Update Rule Chain

    Args:
        json_data (dict): Rule chain data

    Returns:
        Any: JSON response with created/updated rule chain
    """
    endpoint = "ruleChain"
    return await make_thingsboard_request(endpoint, method="post", json_data=json_data)


@mcp.tool()
async def delete_rule_chain(ruleChainId: str) -> Any:
    """Delete Rule Chain

    Args:
        ruleChainId (str): Rule Chain ID

    Returns:
        Any: JSON response
    """
    endpoint = f"ruleChain/{ruleChainId}"
    return await make_thingsboard_request(endpoint, method="delete")


@mcp.tool()
async def get_notification_requests(
    pageSize: int,
    page: int,
    textSearch: Optional[str] = None,
    sortProperty: Optional[str] = None,
    sortOrder: Optional[str] = None,
) -> Any:
    """Get Notification Requests

    Args:
        pageSize (int): Maximum amount of entities in a one page
        page (int): Page number (starts from 0)
        textSearch (Optional[str]): Text search
        sortProperty (Optional[str]): Property to sort by
        sortOrder (Optional[str]): Sort order (ASC or DESC)

    Returns:
        Any: JSON response with notification requests
    """
    endpoint = "notification/requests"
    params = {"pageSize": pageSize, "page": page}

    if textSearch is not None:
        params["textSearch"] = textSearch

    if sortProperty is not None:
        params["sortProperty"] = sortProperty

    if sortOrder is not None:
        params["sortOrder"] = sortOrder

    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def acknowledge_notification_request(notificationRequestId: str) -> Any:
    """Acknowledge Notification Request

    Args:
        notificationRequestId (str): Notification Request ID

    Returns:
        Any: JSON response
    """
    endpoint = f"notification/request/{notificationRequestId}/ack"
    return await make_thingsboard_request(endpoint, method="post")


@mcp.tool()
async def get_notification_delivery_methods() -> Any:
    """Get Notification Delivery Methods

    Returns:
        Any: JSON response with available delivery methods
    """
    endpoint = "notification/deliveryMethods"
    return await make_thingsboard_request(endpoint, method="get")


@mcp.tool()
async def find_entities_by_query(json_data: dict) -> Any:
    """Find entities by query

    Args:
        json_data (dict): The query specification. Should contain entityFilter, pageLink, and other query parameters.

    Returns:
        Any: JSON response with found entities
    """
    endpoint = "entitiesQuery/find"
    return await make_thingsboard_request(endpoint, method="post", json_data=json_data)


@mcp.tool()
async def count_entities_by_query(json_data: dict) -> Any:
    """Count entities by query

    Args:
        json_data (dict): The query specification. Should contain entityFilter.

    Returns:
        Any: JSON response with entity count
    """
    endpoint = "entitiesQuery/count"
    return await make_thingsboard_request(endpoint, method="post", json_data=json_data)


@mcp.tool()
async def find_entity_keys_by_query(
    json_data: dict,
    timeseries: Optional[bool] = None,
    attributes: Optional[bool] = None,
    scope: Optional[str] = None,
) -> Any:
    """Find entity keys by query

    Args:
        json_data (dict): The query specification. Should contain entityFilter.
        timeseries (Optional[bool]): Whether to include timeseries keys
        attributes (Optional[bool]): Whether to include attribute keys
        scope (Optional[str]): Attribute scope (SERVER_SCOPE, SHARED_SCOPE, CLIENT_SCOPE)

    Returns:
        Any: JSON response with entity keys
    """
    endpoint = "entitiesQuery/find/keys"
    params = {}

    if timeseries is not None:
        params["timeseries"] = str(timeseries).lower()

    if attributes is not None:
        params["attributes"] = str(attributes).lower()

    if scope is not None:
        params["scope"] = scope

    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def get_entity_by_id(entityType: str, entityId: str) -> Any:
    """Get Entity by ID

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID

    Returns:
        Any: JSON response
    """
    endpoint = f"entity/{entityType}/{entityId}"
    params = None
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_entities_by_ids(entityType: str, entityIds: str) -> Any:
    """Get Entities by IDs

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityIds (str): Comma-separated list of entity IDs

    Returns:
        Any: JSON response
    """
    endpoint = f"entities/{entityType}"
    params = {"entityIds": entityIds}
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def delete_entity(entityType: str, entityId: str) -> Any:
    """Delete Entity

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID

    Returns:
        Any: JSON response
    """
    endpoint = f"entity/{entityType}/{entityId}"
    params = None
    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def save_entity_telemetry(
    entityType: str, entityId: str, scope: str, json_data: dict
) -> Any:
    """Save Entity Telemetry

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        scope (str): The scope of the telemetry
        json_data (dict): The telemetry data

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/timeseries/{scope}"
    params = None
    return await make_thingsboard_request(
        endpoint, method="post", params=params, json_data=json_data
    )


@mcp.tool()
async def get_entity_timeseries(
    entityType: str,
    entityId: str,
    keys: str,
    startTs: str,
    endTs: str,
    interval: Optional[int] = None,
    limit: Optional[int] = None,
    agg: Optional[str] = None,
) -> Any:
    """Get Entity Timeseries

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        keys (str): Comma-separated list of keys
        startTs (str): Start timestamp in milliseconds
        endTs (str): End timestamp in milliseconds
        interval (Optional[int]): Aggregation interval in milliseconds
        limit (Optional[int]): Max values to return
        agg (Optional[str]): Aggregation function (MIN, MAX, AVG, SUM, COUNT, NONE)

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/values/timeseries"
    params = {"keys": keys, "startTs": startTs, "endTs": endTs}
    if interval:
        params["interval"] = interval
    if limit:
        params["limit"] = limit
    if agg:
        params["agg"] = agg
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def get_entity_latest_timeseries(
    entityType: str, entityId: str, keys: Optional[str] = None
) -> Any:
    """Get Entity Latest Timeseries

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        keys (Optional[str]): Comma-separated list of keys

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/values/timeseries"
    params = {}
    if keys:
        params["keys"] = keys
    return await make_thingsboard_request(endpoint, method="get", params=params)


@mcp.tool()
async def delete_entity_timeseries(
    entityType: str,
    entityId: str,
    keys: str,
    deleteAllDataForKeys: Optional[bool] = None,
    startTs: Optional[str] = None,
    endTs: Optional[str] = None,
    deleteLatest: Optional[bool] = None,
    rewriteLatestIfDeleted: Optional[bool] = None,
) -> Any:
    """Delete Entity Timeseries

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        keys (str): Comma-separated list of keys to delete
        deleteAllDataForKeys (Optional[bool]): If true, all data for specified keys will be deleted
        startTs (Optional[str]): Start timestamp in milliseconds (required if deleteAllDataForKeys is false)
        endTs (Optional[str]): End timestamp in milliseconds (required if deleteAllDataForKeys is false)
        deleteLatest (Optional[bool]): If true, latest values for specified keys will be deleted
        rewriteLatestIfDeleted (Optional[bool]): If true, latest value will be rewritten if it was removed

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/timeseries/delete"
    params = {"keys": keys}

    if deleteAllDataForKeys is not None:
        params["deleteAllDataForKeys"] = str(deleteAllDataForKeys).lower()

    if startTs is not None:
        params["startTs"] = startTs

    if endTs is not None:
        params["endTs"] = endTs

    if deleteLatest is not None:
        params["deleteLatest"] = str(deleteLatest).lower()

    if rewriteLatestIfDeleted is not None:
        params["rewriteLatestIfDeleted"] = str(rewriteLatestIfDeleted).lower()

    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def delete_entity_attributes(
    entityType: str, entityId: str, scope: str, keys: str
) -> Any:
    """Delete Entity Attributes

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityId (str): The entity ID
        scope (str): The scope of attributes (SERVER_SCOPE, SHARED_SCOPE, CLIENT_SCOPE)
        keys (str): Comma-separated list of keys to delete

    Returns:
        Any: JSON response
    """
    endpoint = f"plugins/telemetry/{entityType}/{entityId}/{scope}"
    params = {"keys": keys}

    return await make_thingsboard_request(endpoint, method="delete", params=params)


@mcp.tool()
async def get_entities_by_ids(entityType: str, entityIds: str) -> Any:
    """Get Entities by IDs

    Args:
        entityType (str): The entity type (DEVICE, ASSET, etc.)
        entityIds (str): Comma-separated list of entity IDs

    Returns:
        Any: JSON response
    """
    endpoint = f"entities/{entityType}"
    params = {"entityIds": entityIds}
    return await make_thingsboard_request(endpoint, method="get", params=params)


def is_valid_transport(transport: str) -> bool:
    valid_transports = get_args(fastmcp.server.server.Transport)
    if transport not in valid_transports:
        print(
            f"Invalid MCP server transport: '{transport}'!\nValid transports: '{valid_transports}'"
        )
        return False
    return True


if __name__ == "__main__":
    if MCP_SERVER_TRANSPORT is None or not is_valid_transport(MCP_SERVER_TRANSPORT):
        print("Missing or invalid MCP_SERVER_TRANSPORT environment variable")
        sys.exit(1)
    if THINGSBOARD_API_BASE is None:
        print("Missing THINGSBOARD_API_BASE environment variable")
        sys.exit(1)
    if THINGSBOARD_USERNAME is None:
        print("Missing THINGSBOARD_USERNAME environment variable")
        sys.exit(1)
    if THINGSBOARD_PASSWORD is None:
        print("Missing THINGSBOARD_PASSWORD environment variable")
        sys.exit(1)

    auth_token = get_auth_token(THINGSBOARD_USERNAME, THINGSBOARD_PASSWORD)

    # noinspection PyTypeChecker
    mcp.run(transport=MCP_SERVER_TRANSPORT)
