# User Testing Guide

This guide provides step-by-step instructions for manually testing the HiveInvestor application. It is intended for human testers to verify the application's functionality from a user's perspective.

## Prerequisites

Before testing, ensure the local development environment is running:

1.  **Backend:**
    ```bash
    # Terminal 1
    cd backend
    source host_venv/bin/activate  # or venv/bin/activate
    uvicorn app.main:app --reload
    ```
    *Backend should be running at `http://localhost:8000`*

2.  **Frontend:**
    ```bash
    # Terminal 2
    cd frontend
    npm run dev
    ```
    *Frontend should be running at `http://localhost:5173` (or similar)*

---

## Epic 0: Setup and Connectivity

### Test 0.1: Verify Backend Connectivity
1.  Open a browser and navigate to `http://localhost:8000/`.
2.  **Expected Result:** You should see a JSON response: `{"Hello": "Brave New World"}`.
3.  **Status:** [ ] Pass / [ ] Fail

### Test 0.2: Verify Frontend Home Page
1.  Open a browser and navigate to `http://localhost:5173/`.
2.  **Expected Result:** You should see the HiveInvestor Home page with the title "Welcome to HiveInvestor" and navigation links (Home, Register, Login).
3.  **Status:** [ ] Pass / [ ] Fail

---

## Epic 1: User Management

### Test 1.1: User Registration (Success)
1.  Navigate to `http://localhost:5173/register`.
2.  Enter a valid **Email** (e.g., `testuser@example.com`).
3.  Enter a **Username** (e.g., `testuser`).
4.  Enter a **Password** that meets criteria (e.g., `StrongP@ss1!`).
    *   *Criteria: 8+ chars, 1 uppercase, 1 lowercase, 1 number, 1 special char.*
5.  Enter the same password in **Confirm Password**.
6.  Click **Register**.
7.  **Expected Result:**
    *   A success message "Registration successful!" appears.
    *   You are redirected to the Home page (or Login page, depending on current flow).
    *   *(Optional)* Check backend logs or Firestore to verify user creation.
8.  **Status:** [ ] Pass / [ ] Fail

### Test 1.2: User Registration (Validation Failure)
1.  Navigate to `http://localhost:5173/register`.
2.  Enter an invalid **Email** (e.g., `notanemail`).
    *   **Expected:** Error message "Invalid email format".
3.  Enter a **Password** (e.g., `weak`).
    *   **Expected:** Error message listing missing requirements (length, uppercase, etc.).
4.  Enter mismatching **Confirm Password**.
    *   **Expected:** Error message "Passwords do not match".
5.  **Status:** [ ] Pass / [ ] Fail

### Test 1.3: User Login (Success)
*Prerequisite: Complete Test 1.1 successfully.*
1.  Navigate to `http://localhost:5173/login`.
2.  Enter the **Email** registered in Test 1.1.
3.  Enter the **Password** registered in Test 1.1.
4.  Click **Login**.
5.  **Expected Result:**
    *   You are redirected to the Home page.
    *   (Technical Check): Open Developer Tools -> Application -> Local Storage (or Console logs if implemented) to verify a JWT token is received/stored.
6.  **Status:** [ ] Pass / [ ] Fail

### Test 1.4: User Login (Failure)
1.  Navigate to `http://localhost:5173/login`.
2.  Enter an unregistered **Email** or a wrong **Password**.
3.  Click **Login**.
4.  **Expected Result:** An error message "Incorrect email or password" (or similar) appears.
5.  **Status:** [ ] Pass / [ ] Fail

---

## Epic 2: Portfolio Management

### Test 2.1: Initialize Portfolio (via API Docs)
*Note: Frontend UI for this is not yet implemented. Use Swagger UI.*

1.  **Login via API Docs:**
    *   Go to `http://localhost:8000/docs`.
    *   Click the **Authorize** button (top right).
    *   Enter `username` (email from Test 1.1) and `password`.
    *   Click **Authorize**, then **Close**.
2.  **Create Portfolio:**
    *   Find `POST /api/v1/portfolios/`.
    *   Click **Try it out** -> **Execute**.
    *   **Expected Result:** Response code `201 Created`. JSON body shows `"cash_balance": 100000.0`.
3.  **Verify Portfolio Retrieval:**
    *   Find `GET /api/v1/portfolios/me`.
    *   Click **Try it out** -> **Execute**.
    *   **Expected Result:** Response code `200 OK`. JSON body matches the created portfolio.
4.  **Duplicate Creation Check:**
    *   Execute `POST /api/v1/portfolios/` again.
    *   **Expected Result:** Response code `400 Bad Request`.
5.  **Status:** [ ] Pass / [ ] Fail

### Test 2.2: Get Stock Quote (via API Docs)
1.  **Get Quote:**
    *   Find `GET /api/v1/market/quote/{symbol}`.
    *   Click **Try it out**.
    *   Enter `symbol`: `AAPL`.
    *   Click **Execute**.
    *   **Expected Result:** Response code `200 OK`. JSON body shows `price`, `change`, etc. (Note: If API key is invalid/mock, it might return error or mock data depending on config. Currently configured with 'mock-key', so expect 404 or 503 unless key is set).
2.  **Invalid Symbol:**
    *   Enter `symbol`: `INVALID123`.
    *   Click **Execute**.
    *   **Expected Result:** Response code `404 Not Found` or `503` depending on API response.
3.  **Status:** [ ] Pass / [ ] Fail

### Test 2.3: Execute Trade (via API Docs)
1.  **Buy Stock:**
    *   Find `POST /api/v1/trade/`.
    *   Click **Try it out**.
    *   Enter JSON Request:
        ```json
        {
          "symbol": "AAPL",
          "quantity": 10,
          "type": "BUY"
        }
        ```
    *   Click **Execute**.
    *   **Expected Result:** Response code `200 OK`. JSON shows `total_amount` (approx Price*10 + 10).
2.  **Verify Portfolio Update:**
    *   Find `GET /api/v1/portfolios/me`.
    *   Click **Execute**.
    *   **Expected Result:** `cash_balance` decreased by total amount. `holdings` includes AAPL: 10.
3.  **Sell Stock:**
    *   Find `POST /api/v1/trade/`.
    *   Enter JSON Request:
        ```json
        {
          "symbol": "AAPL",
          "quantity": 5,
          "type": "SELL"
        }
        ```
    *   Click **Execute**.
    *   **Expected Result:** Response code `200 OK`.
4.  **Verify Portfolio Update (Sell):**
    *   Execute `GET /api/v1/portfolios/me` again.
    *   **Expected Result:** `cash_balance` increased. `holdings` AAPL quantity is 5.
5.  **Status:** [ ] Pass / [ ] Fail

### Test 2.4: Dashboard & Trading (UI)
1.  **Navigate to Dashboard:**
    *   Log in to the application.
    *   Go to `/dashboard` (or click Dashboard link if available).
    *   **Expected Result:** You see "Cash Balance", "Total Portfolio Value", "Holdings", "Transaction History", and "Execute Trade" form.
2.  **Buy Stock UI:**
    *   Enter Symbol: `AAPL`.
    *   Enter Qty: `2`.
    *   Select Type: `BUY`.
    *   Click **Submit Trade**.
    *   **Expected Result:** Success message appears. Holdings table updates to show AAPL (or increase quantity). Cash balance decreases. Transaction History adds a row.
3.  **Sell Stock UI:**
    *   Enter Symbol: `AAPL`.
    *   Enter Qty: `1`.
    *   Select Type: `SELL`.
    *   Click **Submit Trade**.
    *   **Expected Result:** Success message. Holdings table updates (quantity decreases). Cash balance increases.
4.  **Status:** [ ] Pass / [ ] Fail
