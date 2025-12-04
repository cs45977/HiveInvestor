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
    *   You are **automatically logged in and redirected to the `/dashboard` page**.
    *   The navigation bar shows "Logged in as: testuser" and a "Logout" button.
    *   *(Optional)* Check Firestore at `http://127.0.0.1:4000/firestore` to verify user creation in the `users` collection with a `role` field.
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
*Prerequisite: Complete Test 1.1 successfully, or have an existing registered user.*
1.  Navigate to `http://localhost:5173/login`.
2.  Enter the **Email** registered in Test 1.1.
3.  Enter the **Password** registered in Test 1.1.
4.  Click **Login**.
5.  **Expected Result:**
    *   You are **redirected to the `/dashboard` page**.
    *   The navigation bar shows "Logged in as: [your username]" and a "Logout" button.
    *   (Technical Check): Open Developer Tools -> Application -> Local Storage to verify a `token` and `user` object are stored.
6.  **Status:** [ ] Pass / [ ] Fail

### Test 1.4: User Login (Failure)
1.  Navigate to `http://localhost:5173/login`.
2.  Enter an unregistered **Email** or a wrong **Password**.
3.  Click **Login**.
4.  **Expected Result:** An error message "Incorrect email or password" (or similar) appears below the form.
5.  **Status:** [ ] Pass / [ ] Fail

### Test 1.5: User Profile Management
*Prerequisite: Logged in as a registered user.*
1.  **Navigate to Profile:**
    *   Click the "Profile" link in the navigation bar (or go to `/profile`).
    *   **Expected Result:** You see the "User Profile" page with your Email (disabled) and Username (editable).
2.  **Update Username:**
    *   Change the **Username** to a new value (e.g., `newusername`).
    *   Click **Update Profile**.
    *   **Expected Result:** Success message "Profile updated successfully" appears.
    *   The navigation bar now displays "Logged in as: newusername".
3.  **Verify Persistence:**
    *   Refresh the page.
    *   **Expected Result:** The Username field still shows `newusername`.
4.  **Status:** [ ] Pass / [ ] Fail

---

## Epic 2: Portfolio Management

### Test 2.1: Portfolio Initialization (Automatic)
*Prerequisite: Logged in as a new user.*
1.  **Navigate to Dashboard:**
    *   Click the "Dashboard" link.
    *   **Expected Result:**
        *   The Dashboard page loads.
        *   "Cash Balance" shows `$100,000.00`.
        *   "Total Portfolio Value" shows `$100,000.00`.
        *   "Holdings" table is empty.
2.  **Status:** [ ] Pass / [ ] Fail

### Test 2.2: Dashboard & Trading (UI)
1.  **Buy Stock:**
    *   On the Dashboard, find the "Execute Trade" form.
    *   Enter Symbol: `AAPL`.
    *   Enter Qty: `10`.
    *   Select Type: `BUY`.
    *   Click **Submit Trade**.
    *   **Expected Result:**
        *   Success message appears.
        *   "Holdings" table adds a row for AAPL with Qty 10.
        *   "Cash Balance" decreases by (Price * 10 + Commission).
        *   "Transaction History" adds a BUY record.
2.  **Sell Stock:**
    *   Enter Symbol: `AAPL`.
    *   Enter Qty: `5`.
    *   Select Type: `SELL`.
    *   Click **Submit Trade**.
    *   **Expected Result:**
        *   Success message appears.
        *   "Holdings" table updates AAPL Qty to 5.
        *   "Cash Balance" increases by (Price * 5 - Commission).
        *   "Transaction History" adds a SELL record.
3.  **Verify Real-Time Valuation:**
    *   Check the "Holdings" table.
    *   **Expected Result:**
        *   "Last Price" column shows the current market price (fetched live).
        *   "Market Value" equals Quantity * Last Price.
        *   "Total Portfolio Value" equals Cash + Sum of Market Values.
4.  **Insufficient Funds (Validation):**
    *   Try to BUY a large quantity (e.g., 100000 AAPL) that exceeds cash.
    *   **Expected Result:** Error message "Insufficient funds" (or similar) appears.
5.  **Status:** [ ] Pass / [ ] Fail

### Test 2.3: Transaction Cancellation
*Prerequisite: Create a PENDING order (see Test 5.3 Limit Order).*
1.  **Navigate to Dashboard.**
2.  **Locate Pending Order:**
    *   Find the transaction in "Transaction History" with status `PENDING`.
3.  **Cancel Order:**
    *   Click the **Cancel** button in the "Action" column.
    *   Confirm the dialog.
4.  **Expected Result:**
    *   Success message appears.
    *   The transaction status updates to `CANCELLED` (or `EXECUTED` if it magically filled, but expected Cancelled).
    *   The Cancel button disappears.
5.  **Status:** [ ] Pass / [ ] Fail

---

## Epic 3: Performance & Leaderboards

### Test 3.1: Trigger Evaluation (Admin)
*Note: This simulates the daily scheduled job.*
1.  **Login via API Docs**.
2.  Find `POST /api/v1/admin/evaluate`.
3.  Click **Execute**.
4.  **Expected Result**: 200 OK. "Evaluation triggered successfully". This updates total values, takes snapshots, and generates leaderboards.
5.  **Status:** [ ] Pass / [ ] Fail

### Test 3.2: View Leaderboard (UI)
1.  Navigate to `/leaderboard`.
2.  Select different time windows (1d, 7d, etc.).
3.  **Expected Result**:
    *   If data exists (after triggering evaluation and having history), a table of users ranked by PPG appears.
    *   If no data, "No data available" message.
4.  **Status:** [ ] Pass / [ ] Fail

---

## Epic 5: Advanced Research & Trading

### Test 5.1: Advanced Trade View & Symbol Search
1.  **Navigate to Trade Page:**
    *   Click the "Trade" link in the navigation bar (or navigate to `/trade`).
    *   **Expected Result:** A split-pane view loads with a Research Panel (Left) and Order Entry Panel (Right).
2.  **Search Symbol:**
    *   In the search bar, enter `GOOG`.
    *   Click "Search" or press Enter.
    *   **Expected Result:**
        *   The **Quote Header** updates to show GOOG price data and **Company Name**.
        *   The **Chart** updates to show GOOG price history.
        *   The **Order Entry Form** updates the symbol to GOOG.
        *   *If you own GOOG:* The Order Entry Form displays "You own: X shares @ Avg. $Y".
3.  **Status:** [ ] Pass / [ ] Fail

### Test 5.2: Advanced Charting Controls
*Prerequisite: On the Trade page with a symbol loaded.*
1.  **Change Timeframe:**
    *   Click "1D", "1M", "1Y".
    *   **Expected Result:** The chart updates its data granularity and range.
2.  **Change Chart Type:**
    *   Click "Line".
    *   **Expected Result:** The chart switches from Candlestick to a Line chart.
    *   Click "Candle".
    *   **Expected Result:** The chart switches back to Candlestick.
3.  **Add Overlay:**
    *   Check "Index Futures (ES)".
    *   **Expected Result:** An orange line (ES) overlays the main chart.
    *   Type `MSFT` in the "Compare..." input and press Enter.
    *   **Expected Result:** A purple line (MSFT) overlays the main chart.
4.  **Status:** [ ] Pass / [ ] Fail

### Test 5.3: Limit Order Execution
*Prerequisite: On the Trade page.*
1.  **Setup Limit Buy:**
    *   Select **Action:** BUY.
    *   Select **Type:** LIMIT.
    *   Enter **Quantity:** 10.
    *   Enter **Limit Price:** A price significantly *lower* than the current market price (e.g., if Price is 150, enter 100).
    *   Select **TIF:** GTC.
    *   Click **Review Order**.
2.  **Confirmation Modal:**
    *   **Expected Result:** A modal appears summarizing: BUY 10 @ $100 Limit (GTC).
    *   Click **Confirm**.
3.  **Verify Pending Order:**
    *   **Expected Result:** Success message "Order Placed Successfully".
    *   Navigate to **Dashboard**.
    *   Check "Transaction History". The order might not execute immediately if the limit price wasn't met (in a real system). *Note: In the current mock/MVP, the backend might execute it immediately or create a transaction depending on logic. If it's a passive limit order, it might just sit in a database, but the current MVP transaction history usually records executed trades. Verify if PENDING orders are visible.* (Currently, the MVP executes or rejects; PENDING state logic is partial).
4.  **Status:** [ ] Pass / [ ] Fail

### Test 5.4: Market Overview (Watchlist)
1.  **Navigate to Dashboard or Home:**
    *   **Expected Result:** A "Market Overview" section is visible.
    *   It displays quotes for "Mag 7" stocks (AAPL, MSFT, GOOG, etc.).
    *   Prices and changes are color-coded (Green/Red).
2.  **Status:** [ ] Pass / [ ] Fail
