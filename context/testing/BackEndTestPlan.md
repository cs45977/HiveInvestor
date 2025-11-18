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
        2.  Send a GET request to the "Hello World" endpoint.
        3.  Verify the response status code is 200.
        4.  Verify the response body contains "Hello World".

### Epic 1: User Management and Authentication

*   **Story 1.1: User Registration API Endpoint**
    *   **Test Instructions:**
        1.  **Happy Path:**
            *   Send a POST request to `/api/v1/users/register` with valid user data (username, email, password).
            *   Verify the response status code is 201 (Created).
            *   Verify the user is created in Firestore with a hashed password.
        2.  **Duplicate Email:**
            *   Attempt to register with an email that already exists.
            *   Verify the response status code is 400 (Bad Request) or 409 (Conflict).
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
            *   Send a GET request to `/api/v1/users/me` (or similar) with the JWT in the Authorization header.
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
            *   Register and log in a new user.
            *   Verify that a portfolio is automatically created for the user with $100,000 cash balance.
            *   Verify the portfolio is stored in Firestore.

*   **Story 2.2: External Market Data API Integration**
    *   **Test Instructions:**
        1.  **Get Quote:**
            *   Send a GET request to `/api/v1/market/quote/{symbol}` for a known stock symbol (e.g., AAPL).
            *   Verify the response status code is 200.
            *   Verify the response contains expected market data (price, volume, etc.).
        2.  **Invalid Symbol:**
            *   Send a GET request for a non-existent symbol.
            *   Verify the response status code is 404 (Not Found) or appropriate error.

*   **Story 2.3: Buy/Sell Trade API Endpoint**
    *   **Test Instructions:**
        1.  **Buy Stock (Happy Path):**
            *   Log in a user with an initialized portfolio.
            *   Send a POST request to `/api/v1/portfolio/{user_id}/trade` with a BUY order (symbol, quantity).
            *   Verify the response status code is 200.
            *   Verify the cash balance is updated (decreased by total cost + commission).
            *   Verify the security holdings are updated (shares added, average cost calculated).
            *   Verify a transaction record is created.
        2.  **Buy Stock (Insufficient Funds):**
            *   Attempt a BUY order that exceeds the user's cash balance.
            *   Verify the response status code is 400.
        3.  **Sell Stock (Happy Path):**
            *   Log in a user with an initialized portfolio and existing shares of a security.
            *   Send a POST request to `/api/v1/portfolio/{user_id}/trade` with a SELL order.
            *   Verify the response status code is 200.
            *   Verify the cash balance is updated (increased by total proceeds - commission).
            *   Verify the security holdings are updated (shares removed).
            *   Verify a transaction record is created.
        4.  **Sell Stock (Insufficient Shares):**
            *   Attempt a SELL order for more shares than the user holds.
            *   Verify the response status code is 400.
        5.  **Invalid Trade Type/Input:**
            *   Attempt a trade with an invalid type or malformed input.
            *   Verify the response status code is 422.

*   **Story 2.6: Transaction History Display**
    *   **Test Instructions:**
        1.  **Get Transactions (Authenticated):**
            *   Log in a user and perform several trades.
            *   Send a GET request to `/api/v1/portfolio/{user_id}/transactions` with the JWT.
            *   Verify the response status code is 200 and contains a list of transactions.
        2.  **Get Transactions (Unauthenticated):**
            *   Send a GET request without a JWT.
            *   Verify the response status code is 401.

### Epic 3: Rolling Performance Evaluation and Leaderboards

*   **Story 3.1: PPG Calculation Logic**
    *   **Test Instructions:**
        1.  **Unit Test PPG Calculation:**
            *   Create mock portfolio data with known starting and current values.
            *   Call the PPG calculation function directly.
            *   Verify the calculated PPG is correct.
        2.  **Edge Cases:**
            *   Test with zero starting value (should handle gracefully, e.g., return 0 or error).
            *   Test with negative gains/losses.

*   **Story 3.2: Scheduled Portfolio Evaluation (Cloud Functions/Cloud Run Jobs)**
    *   **Test Instructions:**
        1.  **Trigger Evaluation:**
            *   Manually trigger the Cloud Function/Cloud Run Job (or simulate its trigger).
            *   Verify that the job runs successfully.
            *   Verify that `last_evaluated_at` timestamps in portfolios are updated.
            *   Verify that new leaderboard entries are created/updated in Firestore.
        2.  **Data Integrity:**
            *   After evaluation, check a sample of user portfolios and leaderboard entries to ensure consistency and correctness of PPG values.

*   **Story 3.3: Leaderboard API Endpoints**
    *   **Test Instructions:**
        1.  **Get 1-Day Leaderboard:**
            *   Ensure leaderboard data exists for the 1-day period.
            *   Send a GET request to `/api/v1/leaderboard/1day`.
            *   Verify the response status code is 200 and contains a sorted list of leaderboard entries.
        2.  **Get All Leaderboards:**
            *   Repeat for 7-day, 30-day, and 90-day leaderboards.
        3.  **Empty Leaderboard:**
            *   Test when no data is available for a specific period (e.g., return empty list or appropriate message).

