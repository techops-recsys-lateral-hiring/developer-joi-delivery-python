# Inventory Health API Changes

## Objective
This document explains how the `/inventory/health` API was implemented, what files changed, why each change exists, and how to reason backward from the running endpoint to the underlying code.

## Problem Before the Change
The route `GET /inventory/health?store_id=store101` existed, but it only returned HTTP `200 OK` with an empty body.

Before the implementation:
- `src/joi_delivery/controller/inventory_controller.py` had a stub endpoint.
- There was no service dedicated to inventory health logic.
- There was no response model describing the endpoint contract.
- The controller test only checked status code and had a placeholder comment for mocking.

## Final API Contract
The endpoint now returns structured store inventory health data:

```json
{
  "store_id": "store101",
  "store_name": "Fresh Picks",
  "total_products": 3,
  "in_stock_products": 3,
  "healthy_products": 3,
  "low_stock_products": 0,
  "out_of_stock_products": 0,
  "products": [
    {
      "product_id": "product101",
      "product_name": "Wheat Bread",
      "available_stock": 30,
      "threshold": 10,
      "health_status": "healthy"
    }
  ]
}
```

If the `store_id` does not exist, the endpoint returns:

```json
{
  "detail": "Store not found for store_id=missing-store"
}
```

with HTTP `404`.

## Testing With curl
Use these commands after starting the app locally on `http://localhost:8020`.

### Success case

```bash
curl "http://localhost:8020/inventory/health?store_id=store101"
```

Sample response:

```json
{
  "store_id": "store101",
  "store_name": "Fresh Picks",
  "total_products": 3,
  "in_stock_products": 3,
  "healthy_products": 3,
  "low_stock_products": 0,
  "out_of_stock_products": 0,
  "products": [
    {
      "product_id": "product101",
      "product_name": "Wheat Bread",
      "available_stock": 30,
      "threshold": 10,
      "health_status": "healthy"
    },
    {
      "product_id": "product102",
      "product_name": "Spinach",
      "available_stock": 30,
      "threshold": 10,
      "health_status": "healthy"
    },
    {
      "product_id": "product103",
      "product_name": "Crackers",
      "available_stock": 30,
      "threshold": 10,
      "health_status": "healthy"
    }
  ]
}
```

### Unknown store case

```bash
curl "http://localhost:8020/inventory/health?store_id=missing-store"
```

Sample response:

```json
{
  "detail": "Store not found for store_id=missing-store"
}
```

## Health Rules
Each product is classified with a `health_status` using these rules:

- `out_of_stock`: `available_stock == 0`
- `low_stock`: `available_stock <= threshold`
- `healthy`: `available_stock > threshold`

These rules are implemented in `InventoryService._resolve_health_status()`.

## Files Changed

### 1. `src/joi_delivery/controller/models.py`
Added two new response models:

- `InventoryProductHealth`
- `InventoryHealthResponse`

Why:
- FastAPI already uses Pydantic models for request and response contracts in the cart API.
- The inventory endpoint needed a formal schema so the controller can return validated JSON.

How to reverse engineer it:
- Start from the route decorator in `inventory_controller.py`.
- Follow the `response_model=InventoryHealthResponse`.
- Open this file to see the exact JSON structure the API promises.

### 2. `src/joi_delivery/service/inventory_service.py`
Created a new service to hold inventory-specific business logic.

Main responsibilities:
- Find the requested store.
- Collect all products belonging to that store.
- Compute per-product health.
- Compute store-level summary counts.
- Raise a `404` if the store is missing.

Why:
- The controller should stay thin and only orchestrate HTTP input/output.
- Inventory health calculation is domain logic and belongs in the service layer.

Key methods:
- `get_inventory_health(store_id)`
- `_get_store_by_id(store_id)`
- `_get_products_for_store(store_id)`
- `_build_product_health(product)`
- `_resolve_health_status(available_stock, threshold)`

How to reverse engineer it:
- Start at `get_inventory_health()`.
- Observe that it first validates the store.
- Then it pulls store products from the seeded `grocery_products`.
- Then it maps products into `InventoryProductHealth`.
- Finally, it builds `InventoryHealthResponse`.

### 3. `src/joi_delivery/dependencies.py`
Added `get_inventory_service()`.

Why:
- The cart API already follows a dependency-injection pattern through `Request.app.state`.
- The inventory endpoint now follows the same design instead of manually constructing services inside the controller.

How to reverse engineer it:
- The controller uses `Depends(get_inventory_service)`.
- That dependency reads `request.app.state.inventory_service`.

### 4. `src/joi_delivery/controller/inventory_controller.py`
Replaced the stub implementation with a real endpoint.

Before:
- It accepted `store_id`.
- It returned an empty `Response(status_code=200)`.

After:
- It accepts `store_id`.
- It injects `InventoryService`.
- It returns `inventory_service.get_inventory_health(store_id)`.
- It declares `response_model=InventoryHealthResponse`.

Why:
- This is the HTTP entry point for the feature.
- It now delegates all business logic to the service layer.

How to reverse engineer it:
- The controller is now intentionally small.
- Most of the behavior is in the service layer and response models.

### 5. `src/joi_delivery/main.py`
Registered `InventoryService` in application state.

Added:
- `app.state.inventory_service = InventoryService(...)`

Why:
- The dependency helper needs the service to exist in the FastAPI application state.
- The service requires the seeded `grocery_products` and `stores`.

How to reverse engineer it:
- Application startup calls `initialize_data()`.
- Those seeded objects are passed into the service constructors.
- The inventory service is now initialized alongside user, product, and cart services.

### 6. `tests/controller/test_inventory_controller.py`
Replaced the placeholder test with real contract assertions.

New coverage:
- Valid store returns HTTP `200`.
- Valid store returns correct summary counts.
- Valid store returns a product list with `healthy` status.
- Unknown store returns HTTP `404` with a clear error payload.

Why:
- The previous test only asserted the status code and would not catch regressions in the response body.
- These tests now verify the actual API contract.

How to reverse engineer it:
- Run the tests and inspect the asserted fields.
- The test file describes the intended endpoint behavior from the outside in.

### 7. `README.md`
Updated the inventory health section with a real example response.

Why:
- The README previously showed `// to be implemented`.
- The endpoint is now implemented and should be documented accordingly.

## Data Flow End to End
This is the request path from HTTP call to computed response:

1. Request hits `GET /inventory/health`.
2. FastAPI routes to `fetch_store_inventory_health()` in `inventory_controller.py`.
3. FastAPI injects `InventoryService` using `get_inventory_service()`.
4. The controller calls `inventory_service.get_inventory_health(store_id)`.
5. The service validates the store using seeded store data.
6. The service filters seeded grocery products for the requested store.
7. The service computes `health_status` for each product.
8. The service aggregates store-level summary counts.
9. FastAPI serializes the `InventoryHealthResponse` model to JSON.

## Design Decisions

### Why a new service instead of reusing `ProductService`
`ProductService` only exposes `get_product(product_id, outlet_id)`, which is single-product lookup logic. Inventory health is a store-level concern with aggregation rules, so a dedicated service is cleaner and avoids overloading product lookup responsibilities.

### Why use seeded products instead of `GroceryStore.inventory`
The current seed setup links products to stores through `product.store`, while `GroceryStore.inventory` is not populated during initialization. To avoid changing more domain behavior than necessary, the implementation derives inventory from the existing seeded `grocery_products` list.

### Why raise `HTTPException` in the service
This keeps error handling explicit and produces a correct HTTP `404` from the service path used by the controller. In a larger codebase, this could move into a domain exception plus controller mapping, but the current project structure is simple and consistent with FastAPI usage.

## How to Extend This
If you want to expand the API later, these are the safest next steps:

- Add expiry-based health rules once `expiry_date` semantics are clarified.
- Add sorting so low-stock or out-of-stock items appear first.
- Add filtering options like `status=low_stock`.
- Add unit tests for `_resolve_health_status()` if the logic grows more complex.
- Add a store service if more store-related endpoints are introduced.

## How to Revert the Change
If you need to remove the feature later, reverse these steps:

1. Remove `InventoryService` and its registration in `main.py`.
2. Remove `get_inventory_service()` from `dependencies.py`.
3. Remove `InventoryHealthResponse` and `InventoryProductHealth` from `controller/models.py`.
4. Restore `inventory_controller.py` to a stub or alternate implementation.
5. Revert the test updates in `tests/controller/test_inventory_controller.py`.
6. Revert the README inventory response example.

## Validation Performed
The implementation is intended to be verified with:

```bash
pytest
```

or

```bash
poetry run pytest
```

The expected seeded response for `store101` is:
- `total_products = 3`
- `in_stock_products = 3`
- `healthy_products = 3`
- `low_stock_products = 0`
- `out_of_stock_products = 0`
