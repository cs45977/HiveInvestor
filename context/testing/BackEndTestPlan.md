# Backend Testing Plan: HiveInvestor

This document outlines the testing strategy and specific test cases for the FastAPI backend of the HiveInvestor application. We will focus on unit and integration tests to ensure the correctness and robustness of the API.

## 1. Testing Framework

We will use `pytest` as our primary testing framework for the Python backend, along with `httpx` for testing API endpoints.

## 2. General Testing Principles

*   **Unit Tests:** Focus on individual functions, methods, or classes in isolation. Mock external dependencies (e.g., Firestore, external market data API).
*   **Integration Tests:** Verify the interaction between different components (e.g., API endpoints with business logic and database interactions).
*   **Test Data:** Use consistent, isolated test data for each test case.
*   **Coverage:** Aim for high test coverage, especially for critical business logic.

## 3. Test Plan by Epic and Story

### Epic 0: Setup and "Hello World" Deployment

*   **Story 0.1: Backend Project Initialization (FastAPI)**
    *   **Test Instructions:**
        1.  Ensure the FastAPI application can start without errors.
        2.  Send a GET request to the root endpoint (`/`).
        3.  Verify the response status code is 200.
        4.  Verify the response body contains `{"Hello": "Brave New World"}`.

### Epic 1: User Management and Authentication

*   **Story 1.1: User Registration API Endpoint**
    *   **Test Instructions:**
        1.  **Happy Path:**
            *   Send a POST request to `/api/v1/users/register` with valid user data (username, email, password).
            *   Verify the response status code is 201 (Created).
            *   Verify the user is created in Firestore.
        2.  **Duplicate Email:**
            *   Attempt to register with an email that already exists.
            *   Verify the response status code is 400 (Bad Request).
        3.  **Invalid Input:**
            *   Attempt to register with missing or invalid fields (e.g., malformed email, weak password).
            *   Verify the response status code is 422 (Unprocessable Entity).

*   **Story 1.2: User Login API Endpoint (JWT)**
    *   **Test Instructions:**
        1.  **Happy Path:**
            *   Register a new user.
            *   Send a POST request to `/api/v1/users/login` with the correct email and password.
            *   Verify the response status code is 200.
            *   Verify the response body contains a valid JWT token.
        2.  **Incorrect Password:**
            *   Attempt to log in with a correct email but an incorrect password.
            *   Verify the response status code is 401 (Unauthorized).
        3.  **Non-existent User:**
            *   Attempt to log in with an email not registered in the system.
            *   Verify the response status code is 401 (Unauthorized).
        4.  **Invalid Input:**
            *   Attempt to log in with missing or invalid fields.
            *   Verify the response status code is 422 (Unprocessable Entity).

*   **Story 1.5: User Profile Management (Basic)**
    *   **Test Instructions:**
        1.  **Get Profile (Authenticated):**
            *   Log in a user to obtain a JWT.
            *   Send a GET request to `/api/v1/users/me` with the JWT in the Authorization header.
            *   Verify the response status code is 200 and contains the user's profile data.
        2.  **Get Profile (Unauthenticated):**
            *   Send a GET request to `/api/v1/users/me` without a JWT.
            *   Verify the response status code is 401.
        3.  **Update Profile (Authenticated):**
            *   Log in a user to obtain a JWT.
            *   Send a PUT/PATCH request to `/api/v1/users/me` with updated profile data and the JWT.
            *   Verify the response status code is 200.
            *   Verify the profile data is updated in Firestore.
        4.  **Update Profile (Invalid Input):**
            *   Attempt to update with invalid data.
            *   Verify the response status code is 422.

### Epic 2: Portfolio Management and Trading

*   **Story 2.1: Portfolio Initialization API**
    *   **Test Instructions:**
        1.  **New User Portfolio:**
            *   Register and log in a new user. A portfolio with $100,000 cash balance is automatically created upon first access (or registration if implemented that way).
            *   Send a GET request to `/api/v1/portfolios/me`.
            *   Verify the response status code is 200.
            *   Verify the response contains portfolio data with `$100,000` cash balance.
            *   Verify the portfolio is stored in Firestore.
        2.  **Attempt Duplicate Creation:**
            *   Send a POST request to `/api/v1/portfolios/` for a user who already has a portfolio.
            *   Verify the response status code is 400.

*   **Story 2.2: External Market Data API Integration**
    *   **Test Instructions:**
        1.  **Get Quote (Authenticated):**
            *   Send a GET request to `/api/v1/market/quote/{symbol}` for a known stock symbol (e.g., `AAPL`) with a valid JWT.
            *   Verify the response status code is 200.
            *   Verify the response contains expected market data (price, change, percent_change).
        2.  **Get Quote (Invalid Symbol):**
            *   Send a GET request for a non-existent symbol (e.g., `INVALID_SYM`) with a valid JWT.
            *   Verify the response status code is 404 (Not Found).
        3.  **Get Quote (Unauthenticated):**
            *   Send a GET request to `/api/v1/market/quote/{symbol}` without a JWT.
            *   Verify the response status code is 401.

*   **Story 2.3: Buy/Sell Trade API Endpoint**
    *   **Test Instructions:**
        1.  **Buy Stock (Happy Path):**
            *   Log in a user with an initialized portfolio.
            *   Send a POST request to `/api/v1/trade/` with a valid BUY order (`{"symbol": "AAPL", "quantity": 10, "type": "BUY"}`) and a valid JWT.
            *   Verify the response status code is 200.
            *   Verify the cash balance in the user's portfolio (via `GET /api/v1/portfolios/me`) is updated (decreased by total cost + $10 commission).
            *   Verify the security holdings are updated (shares added, average cost calculated).
            *   Verify a transaction record is created (via `GET /api/v1/transactions/`).
        2.  **Buy Stock (Insufficient Funds):**
            *   Attempt a BUY order that exceeds the user's cash balance with a valid JWT.
            *   Verify the response status code is 400 with detail "Insufficient funds".
        3.  **Sell Stock (Happy Path):**
            *   Log in a user with an initialized portfolio and existing shares of a security (e.g., after a successful BUY trade).
            *   Send a POST request to `/api/v1/trade/` with a valid SELL order (`{"symbol": "AAPL", "quantity": 5, "type": "SELL"}`) and a valid JWT.
            *   Verify the response status code is 200.
            *   Verify the cash balance is updated (increased by total proceeds - $10 commission).
            *   Verify the security holdings are updated (shares removed).
            *   Verify a transaction record is created.
        4.  **Sell Stock (Insufficient Shares):**
            *   Attempt a SELL order for more shares than the user holds with a valid JWT.
            *   Verify the response status code is 400 with detail "Insufficient holdings".
        5.  **Invalid Trade Type/Input:**
            *   Attempt a trade with an invalid type or malformed input with a valid JWT.
            *   Verify the response status code is 422.
        6.  **Unauthenticated Trade:**
            *   Attempt a trade without a JWT.
            *   Verify the response status code is 401.

*   **Story 2.6: Transaction History Display**
    *   **Test Instructions:**
        1.  **Get Transactions (Authenticated):**
            *   Log in a user and perform several trades.
            *   Send a GET request to `/api/v1/transactions/` with the JWT.
            *   Verify the response status code is 200 and contains a list of transactions, sorted by timestamp descending.
        2.  **Get Transactions (Unauthenticated):**
            *   Send a GET request to `/api/v1/transactions/` without a JWT.
            *   Verify the response status code is 401.

### Epic 3: Rolling Performance Evaluation and Leaderboards

*   **Story 3.1 & 3.2: PPG Calculation Logic & Scheduled Portfolio Evaluation**
    *   **Test Instructions:**
        1.  **Manual Trigger:**
            *   Log in a user to obtain a JWT.
            *   Send a POST request to `/api/v1/leaderboard/admin/evaluate` with the JWT.
            *   Verify the response status code is 200 with message "Evaluation triggered successfully".
            *   (Optional but Recommended): Check Firestore to see if `portfolio_snapshots` and `leaderboards` collections are populated.
        2.  **Unit Test PPG Calculation:**
            *   Create mock portfolio data with known starting and current values.
            *   Call the `calculate_ppg` function directly.
            *   Verify the calculated PPG is correct.
        3.  **Edge Cases for PPG:**
            *   Test `calculate_ppg` with zero starting value (should return 0).
            *   Test with negative gains/losses.
        4.  **Unit Test Snapshot Portfolio:**
            *   Call `snapshot_portfolio` directly with mock database and user ID.
            *   Verify that a snapshot document is created in `portfolio_snapshots` with the correct calculated `total_value`.
            *   Test case where snapshot already exists for the day (should not create new one).
        5.  **Unit Test `update_all_portfolios_total_value`:**
            *   Call this function with a mock database.
            *   Verify that `total_value` fields in `portfolios` collection are updated for all users.
            *   Verify `snapshot_portfolio` is called for each user.

*   **Story 3.3: Leaderboard API Endpoints**
    *   **Test Instructions:**
        1.  **Get Leaderboard (Authenticated, Existing Data):**
            *   Ensure evaluation has been triggered (Test 3.1).
            *   Send a GET request to `/api/v1/leaderboard/{window}` (e.g., `1d`, `7d`, `30d`, `90d`) with a valid JWT.
            *   Verify the response status code is 200.
            *   Verify the response contains a `Leaderboard` object with `entries` sorted by `ppg` descending and correct `rank`.
        2.  **Get Leaderboard (Invalid Window):**
            *   Send a GET request to `/api/v1/leaderboard/invalid_window` with a valid JWT.
            *   Verify the response status code is 400.
        3.  **Get Leaderboard (Not Found / No Data):**
            *   Test a scenario where no leaderboard data exists for a period (e.g., if evaluation hasn't run).
            *   Verify the response status code is 404 (Not Found).
        4.  **Get Leaderboard (Unauthenticated):**
            *   Send a GET request to `/api/v1/leaderboard/{window}` without a JWT.
            *   Verify the response status code is 401.