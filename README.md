# Welcome to JOI Delivery
JOI Delivery is built for real life. For the young professional who gets home late and doesn’t have the energy to cook. For the student with an exam tomorrow and an empty fridge tonight. These aren’t exceptions — they’re everyday moments. That’s why JOI Delivery brings food and groceries to your door, fast, fresh, and right when you need them.

Customers struggle with:

- Cluttered browsing experiences that don’t understand their preferences.
- Limited customization when ordering meals or groceries.
- Unclear order status or delivery timelines.
- Poor payment experience, or failed checkouts.
- Lack of timely feedback channels to report a bad experience or appreciate a good one.

JOI Delivery was built not just as another delivery app, but as a thoughtful, technology-first platform that reimagines how essentials reach customers in the most seamless way.

# Introducing JOI Delivery

JOI Delivery, launched in 2024, is a hyperlocal delivery app designed to bring food and groceries to your doorstep in under 45 minutes. With the tagline "Speed meets convenience," it connects customers to nearby restaurants and stores through a seamless digital experience. The app solves the hassle of long wait times and limited local options by offering real-time tracking, instant order updates, and a wide network of trusted vendors.

## Business Goals
- Differentiated Value Proposition & Niche Dominance
- Deliver Unmatched Customer Experience & Loyalty
- Superior Operational Efficiency & Cost Advantage
- Robust & Engaged Partner Ecosystem

## Why they need Thoughtworks help
As JOI Delivery continues to grow and serve more neighborhoods, we’re scaling our platform to handle increasing demand, enhance user experience, and support smarter delivery logistics. They're looking for passionate developers to help us build robust, efficient, and scalable solutions that power everything from order placement to real-time tracking.
Your expertise will directly impact how quickly and reliably customers receive their essentials—and how smoothly local vendors and delivery partners operate within our ecosystem.

### Users/Customers
Sample user profiles are available in the repository to support development and testing scenarios.

| UserId   | FirstName | LastName|
|----------|-----------|---------|
| user101  | John      | Doe     |

### Stores
Sample store data seeded for development purposes only.

| StoreId  | OutletName     |
|----------|----------------|
| store101 | Fresh Picks    |
| store102 | Natural Choice |

### Grocery Products
Dummy Products for Stores to sell and users to buy from.

| ProductId  | ProductName | StoreRefId |
|------------|-------------|------------|
| product101 | Wheat Bread | store101   |
| product102 | Spinach     | store101   |
| product103 | Crackers    | store101   |

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.12
- **Dependency Management**: Poetry
- **Testing**: pytest
- **Code Quality**: Ruff, Black
- **Logging**: Loguru

## Getting Started

### Prerequisites

- Python 3.12+
- Poetry (for dependency management)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd joi-delivery-python
   ```

2. **Install dependencies**
   ```bash
   poetry install --with ci,tests
   ```

3. **Run the application**
   ```bash
   poetry run python -m uvicorn src.main:app --reload
   ```

The application will be available at `http://localhost:8020`

### API Documentation

Once the application is running, you can access:
- **Interactive API docs**: `http://localhost:8020/docs`
- **ReDoc documentation**: `http://localhost:8020/redoc`

## API Endpoints

### Cart Management

#### Add Product to Cart
```http
POST /cart/product
Content-Type: application/json

{
  "user_id": "user101",
  "product_id": "product101",
  "outlet_id": "store101"
}
```

#### View Cart
```http
GET /cart/view?userId=user101
```

### Inventory Health

#### Get Store Inventory Health
```http
GET /inventory/health/{store_id}
```

## Testing

Run the test suite:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest --cov=src
```

## Development

### Code Quality

The project uses several tools to maintain code quality:

- **Ruff**: Fast Python linter
- **Black**: Code formatter
- **pytest**: Testing framework

### Pre-commit Hooks

Install pre-commit hooks:

```bash
poetry run pre-commit install
```