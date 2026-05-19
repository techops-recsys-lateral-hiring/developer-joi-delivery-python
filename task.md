# JOI Delivery Implementation Tasks

## Task 1: Fix Inventory Health

### Goal
Implement the `/inventory/health` endpoint so it returns a meaningful inventory health response for a store instead of only `200 OK`.

### Step 1: Understand the current inventory flow
- Review `src/joi_delivery/controller/inventory_controller.py` to confirm the endpoint behavior and missing logic.
- Review `src/joi_delivery/generator/app_initializer.py` to understand seeded stores and grocery products.
- Review `src/joi_delivery/domain/grocery_product.py` and `src/joi_delivery/domain/grocery_store.py` to identify available inventory fields such as `threshold`, `available_stock`, and `expiry_date`.
- Review `tests/controller/test_inventory_controller.py` to understand the current placeholder test and expected extension point.

### Step 2: Define inventory health output
- Decide the response shape for `/inventory/health?store_id={store_id}`.
- Include store-level summary fields such as `store_id`, `store_name`, `total_products`, `in_stock_products`, `low_stock_products`, and `out_of_stock_products`.
- Include product-level details for each inventory item with at least `product_id`, `product_name`, `available_stock`, `threshold`, and a computed `health_status`.
- Define health rules:
- `out_of_stock` when `available_stock == 0`.
- `low_stock` when `available_stock <= threshold`.
- `healthy` when `available_stock > threshold`.

### Step 3: Add service-layer support
- Create an inventory-focused service or extend the current service layer with inventory health logic.
- Add a method to fetch all products for a given store.
- Add a method to compute product health and store summary metrics.
- Keep the controller thin and move business rules into the service layer.

### Step 4: Add response models
- Add response models in `src/joi_delivery/controller/models.py` or a dedicated inventory model file.
- Define a product inventory health model.
- Define a store inventory health response model.
- Ensure the response is serializable and consistent with FastAPI response model usage already used in the cart endpoints.

### Step 5: Implement endpoint behavior
- Inject the new inventory service using FastAPI dependencies.
- Validate that `store_id` exists.
- Return a structured JSON response for valid stores.
- Return a clear error response for unknown stores.

### Step 6: Add and update tests
- Replace the placeholder inventory controller test with real assertions on the JSON response body.
- Add a test for a valid store with seeded products.
- Add a test for an invalid `store_id`.
- Add unit tests for inventory health calculation rules if the logic is extracted into a service.

### Step 7: Verify end to end
- Run the app locally and call `GET /inventory/health?store_id=store101`.
- Confirm the response matches the agreed schema.
- Run `poetry run pytest` and fix any regressions.
- Update `README.md` with the actual response example once implementation is complete.

## Task 2: Add One Agent Using LangChain and LangGraph

### Goal
Add a single AI agent powered by local Ollama, built with LangChain and LangGraph, and connect it to JOI Delivery in a way that is easy to test and extend.

### Step 1: Define the first agent use case
- Pick one concrete business use case for the first agent.
- Recommended option: `Inventory Health Agent`.
- The agent should answer questions about store inventory health, low-stock products, and stock risks using existing JOI Delivery data.
- Define the initial user input and expected output format before writing code.

### Step 2: Prepare dependencies and project structure
- Add LangChain, LangGraph, and Ollama integration dependencies to the project.
- Create a dedicated package such as `src/joi_delivery/ai/`.
- Add submodules for `llm`, `graph`, `tools`, `prompts`, and `agent_service`.
- Keep AI-specific code isolated from controllers and core domain logic.

### Step 3: Wire Ollama through LangChain
- Configure a local Ollama-backed LLM client for `llama3.2`.
- Add a small adapter or factory for LLM creation so configuration is centralized.
- Verify a basic invocation works locally before building the graph flow.
- Externalize model name and base URL into environment-driven configuration where possible.

### Step 4: Design the LangGraph workflow
- Create a minimal LangGraph state definition for the agent.
- Define graph nodes for `parse user request`, `fetch inventory data`, `reason over inventory state`, and `format final response`.
- Keep the first version single-agent and deterministic in flow, even if it uses LangGraph internally.

### Step 5: Add domain tools for the agent
- Create one or more tools that expose JOI Delivery data safely to the agent.
- Recommended first tool: fetch store inventory health by `store_id`.
- Keep tool outputs structured and compact so the LLM receives clean context.
- Reuse the inventory health service instead of duplicating inventory logic inside the AI module.

### Step 6: Implement an agent service
- Create an application service that receives a prompt or task request and runs the LangGraph workflow.
- Return a structured response containing `user question`, `resolved store context`, `agent answer`, and optional execution metadata for debugging.
- Keep the service callable from HTTP endpoints and tests.

### Step 7: Expose the agent through an API
- Add a new controller for the AI agent, for example `/ai/inventory-agent`.
- Define request and response models.
- Support at least one request containing `store_id` and a natural-language question.
- Return clean error messages when the model is unavailable or the store is unknown.

### Step 8: Add tests for the AI integration
- Add tests for the controller contract.
- Add tests for the agent service with mocked LLM responses.
- Add tests for tool execution and graph flow decisions where practical.
- Keep tests stable by mocking Ollama in automated test runs.

### Step 9: Add developer setup and documentation
- Document local prerequisites in `README.md`: install Ollama, pull `llama3.2`, verify `ollama run llama3.2 "hello"`, and explain how to run the new AI endpoint locally.
- Add example request and response payloads.

### Step 10: Stretch follow-ups after the first agent works
- Add a second tool for product lookup or store lookup.
- Add conversational memory only if there is a real need.
- Add observability for prompts, tool calls, and graph transitions.
- Evaluate whether the agent should remain single-purpose or expand into a multi-agent workflow later.
