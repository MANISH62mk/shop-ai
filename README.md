# SHOPAI — AI-Powered E-Commerce Assistant with Semantic Search & Live Inventory Management

A modern, fully functional college mini-project demonstrating an e-commerce platform equipped with a natural-language semantic shopping assistant, heuristic intent parser, live stock availability verification, simulated checkout, automatic inventory decrement, and real-time admin sales analytics.

---

## 🌟 Project Overview

Traditional e-commerce search engines rely almost purely on exact keyword matching, failing when users search with natural intent, such as:
> *"I need a lightweight laptop for coding under ₹60,000"*

**SHOPAI** solves this by:
1. **Understanding Intent**: Deconstructs user sentences into categories, maximum budget, use cases (e.g., coding, gaming, photography), brand preferences, and semantic keywords.
2. **Relevance Scoring Engine**: Evaluates catalog products with a multi-factor semantic scoring algorithm that balances intent alignment, budget constraints, user ratings, and live stock.
3. **Inventory Guarantees**: Never recommends products with zero stock, clearly alerts users when a queried product is out of stock, and automatically recommends live in-stock alternatives.
4. **Autonomous Stock Deductions**: On placing an order (Cash on Delivery or Demo Card), the system atomically deducts product stock in SQLite and reflects new revenue and unit counts on the Admin Dashboard immediately.
5. **No External LLM Dependency**: Ships with a reliable, offline-ready Python heuristic semantic parser with optional LLM hook capabilities.

---

## 🚀 Tech Stack

| Layer | Technology | Description |
|---|---|---|
| **Frontend** | React 19 + TypeScript | Component-driven UI with type safety |
| **Styling** | Tailwind CSS v4 + Lucide Icons | Responsive, modern startup aesthetic |
| **Backend** | Python FastAPI + Uvicorn | High-performance asynchronous REST API |
| **Database** | SQLite + SQLAlchemy ORM | Lightweight relational storage with atomic transactions |
| **AI / NLP** | Python Regex & Semantic Heuristic Scoring | Offline intent extraction and relevance reasoning |

---

## 🏗️ Architecture & Directory Structure

```
shopai/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint, CORS, startup events
│   ├── database.py              # SQLite connection, engine & seed data loader
│   ├── models.py                # SQLAlchemy ORM models (User, Product, Order, OrderItem, CartItem)
│   ├── schemas.py               # Pydantic request/response validation schemas
│   ├── requirements.txt         # Python dependencies
│   ├── sample_products.csv      # Sample CSV for testing bulk inventory import
│   ├── routes/
│   │   ├── ai.py                # AI search & personalized recommendations endpoints
│   │   ├── products.py          # Catalog browsing, filtering & product details
│   │   ├── cart.py              # Cart operations & stock limit validation
│   │   ├── orders.py            # Atomic checkout & order histories
│   │   ├── admin.py             # KPI metrics, sales charts, CRUD, CSV import
│   │   └── auth.py              # Demo authentication (Customer & Admin)
│   └── services/
│       ├── ai_search.py         # Heuristic intent parser, relevance scoring, out-of-stock handler
│       └── recommendations.py   # Hybrid recommendation engine
├── database/
│   ├── shopai.db                # SQLite database file
│   └── schema.sql               # Relational DDL schema script
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts           # Vite bundler with API proxy to port 8000
│   └── src/
│       ├── types/               # TypeScript interfaces
│       ├── services/api.ts      # Fetch API client
│       ├── context/AppContext.tsx# Global state (Cart, User, Toasts, Views)
│       ├── components/          # Navbar, Footer, AISearchBar, ProductCard, AuthModal, Toast
│       └── pages/               # HomePage, DiscoverPage, ProductDetailPage, CartPage,
│                                # CheckoutPage, OrderSuccessPage, OrdersPage, AdminDashboard
├── test_system.py               # Automated end-to-end verification script
└── README.md                    # Project documentation
```

---

## 📊 Database Schema

### `users`
- `id` (INTEGER, Primary Key)
- `email` (TEXT, Unique)
- `password_hash` (TEXT)
- `name` (TEXT)
- `role` (TEXT: `'customer'` or `'admin'`)
- `created_at` (TIMESTAMP)

### `products`
- `id` (INTEGER, Primary Key)
- `name` (TEXT)
- `category` (TEXT)
- `brand` (TEXT)
- `price` (REAL, INR)
- `stock_quantity` (INTEGER)
- `description` (TEXT)
- `rating` (REAL)
- `tags` (TEXT)
- `image_url` (TEXT)
- `specs` (TEXT, JSON string)
- `created_at` (TIMESTAMP)

### `orders`
- `id` (INTEGER, Primary Key)
- `user_id` (INTEGER, Foreign Key to `users.id`)
- `customer_name` (TEXT)
- `customer_email` (TEXT)
- `customer_phone` (TEXT)
- `shipping_address` (TEXT)
- `payment_method` (TEXT: `'Cash on Delivery'` or `'Demo Card Payment'`)
- `total_amount` (REAL)
- `status` (TEXT: `'Confirmed'`, `'Processing'`, etc.)
- `created_at` (TIMESTAMP)

### `order_items`
- `id` (INTEGER, Primary Key)
- `order_id` (INTEGER, Foreign Key to `orders.id`)
- `product_id` (INTEGER, Foreign Key to `products.id`)
- `product_name` (TEXT)
- `unit_price` (REAL)
- `quantity` (INTEGER)
- `subtotal` (REAL)

### `cart_items`
- `id` (INTEGER, Primary Key)
- `session_id` (TEXT, Index)
- `user_id` (INTEGER, Foreign Key to `users.id`, Nullable)
- `product_id` (INTEGER, Foreign Key to `products.id`)
- `quantity` (INTEGER)
- `created_at` (TIMESTAMP)

---

## ⚡ How to Run the Project

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

---

### Step 1: Start the Backend (FastAPI)

1. Open a terminal in the project root:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the Uvicorn server:
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend URL:* `http://127.0.0.1:8000`
*Interactive Swagger API Docs:* `http://127.0.0.1:8000/docs`

---

### Step 2: Start the Frontend (React + TypeScript)

1. Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```

*Frontend URL:* `http://127.0.0.1:5173`

---

## 🔑 Demo Credentials

Click the **Sign In** button on the Navbar to use the 1-click test credential switchers:

| Role | Email | Password | Permissions |
|---|---|---|---|
| **Demo Customer** | `demo@shopai.com` | `demo123` | Browse, AI search, Cart, Demo Checkout, Orders |
| **Demo Admin** | `admin@shopai.com` | `admin123` | Full Admin Dashboard, Inline Stock Editor, Product CRUD, CSV Import |

---

## 💡 Example AI Natural Language Queries to Try

Test these exact prompts directly in the Hero Search box:

1. **`I need a lightweight laptop for coding under ₹60,000`**
   - *Extracted Intent*: Category: Laptops, Max Budget: ₹60,000, Use Case: Coding, Feature: Lightweight.
   - *Result*: Returns top in-stock laptops like Acer Swift Go 14 (1.25 kg, i5, 16GB RAM) and Asus VivoBook 15 under ₹60,000 with detailed bullet points explaining why each is recommended.

2. **`Show me wireless headphones under 3000`**
   - *Extracted Intent*: Category: Headphones, Max Budget: ₹3,000, Feature: Wireless.
   - *Result*: Recommends boAt Rockerz 550, Noise Two, and OnePlus Bullets Wireless Z2.

3. **`I need a phone with good camera under 25000`**
   - *Extracted Intent*: Category: Smartphones, Max Budget: ₹25,000, Feature: Camera/OIS.
   - *Result*: Recommends Realme 12 Pro 5G and Redmi Note 13 Pro 5G (200MP OIS sensor).

4. **`Suggest something for gaming`**
   - *Extracted Intent*: Use Case: Gaming across categories.
   - *Result*: Highlights Asus TUF Gaming laptop (RTX 3050), Redragon mechanical gaming keyboard, and LG 144Hz monitor.

5. **`Find a monitor for coding`**
   - *Extracted Intent*: Category: Monitors, Use Case: Coding/Ergonomic.
   - *Result*: Highlights BenQ Eye-Care IPS and Dell 90-degree pivot monitor for vertical coding.

6. **Out-of-Stock Demo Query (`Acer Aspire 5`)**:
   - The catalog seeds `Acer Aspire 5 Slim Edition` with `stock_quantity = 0`.
   - *Result*: The AI explicitly alerts that the queried product is Out of Stock and recommends available in-stock alternatives!

---

## 🧪 Testing the Complete Demo Flow (Phase 11)

Follow these exact steps to demonstrate the full end-to-end system:

1. Open `http://127.0.0.1:5173`.
2. In the AI Search Box, type:
   > **"I need a lightweight laptop for coding under ₹60,000"**
3. Review the extracted intent chips and the AI reasoning explanation.
4. Click on the top laptop card (*Acer Swift Go 14*).
5. On the Product Details page, note the stock count (e.g. 7 units available).
6. Click **Add to Cart** or **Buy Now**.
7. In the Cart, proceed to **Checkout**.
8. Select **Cash on Delivery** or **Demo Card Payment** and click **Place Demo Order**.
9. The Order Confirmation page displays the new Order ID and confirms stock deduction.
10. Click **Admin Dashboard** in the navbar (or `/admin`).
11. Observe:
    - **Total Orders** incremented by 1.
    - **Total Revenue** increased by the order amount.
    - **Units Sold** increased.
    - The product's stock decreased by the ordered quantity.
12. Go to the **Fast Inventory Editor** tab in Admin:
    - Click **"Set to 0 (Test Demo)"** on any item.
    - Return to Home, search for that item, and verify that the AI alerts that it is out of stock and recommends available alternatives.

---

## 🔮 Future Improvements

- Add semantic vector embeddings (e.g. ChromaDB / Sentence-Transformers) for vector search alongside heuristic scoring.
- Add real multi-currency support and localized languages.
- Optional SMS / WhatsApp mock notifications via Twilio for order dispatch.
- User review submission and verified buyer ratings.
