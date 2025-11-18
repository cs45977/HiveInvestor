# Frontend Testing Plan: HiveInvestor

This document outlines the testing strategy and specific test cases for the Vue.js frontend of the HiveInvestor application. We will focus on component, integration, and end-to-end tests to ensure a robust and user-friendly interface.

## 1. Testing Framework

We will use `Vitest` for unit and component testing, and `Cypress` for end-to-end (E2E) testing.

## 2. General Testing Principles

*   **Component Tests:** Focus on individual Vue components in isolation, testing their props, events, slots, and rendering logic.
*   **Integration Tests:** Verify the interaction between multiple Vue components or between components and the Vuex/Pinia store.
*   **End-to-End (E2E) Tests:** Simulate real user scenarios across the entire application, interacting with the deployed backend.
*   **User Experience (UX):** Ensure the UI is intuitive, responsive, and provides clear feedback to the user.
*   **Accessibility:** Basic checks for accessibility (e.g., keyboard navigation, ARIA attributes).

## 3. Test Plan by Epic and Story

### Epic 0: Setup and "Hello World" Deployment

*   **Story 0.2: Frontend Project Initialization (Vue.js with Tailwind CSS)**
    *   **Test Instructions:**
        1.  Verify the Vue.js application compiles and runs locally without errors.
        2.  Verify that Tailwind CSS classes are correctly applied and render as expected.
        3.  Verify the "Hello World" component is displayed on the main page.

*   **Story 0.5: GCP Cloud Storage/CDN Deployment for Frontend**
    *   **Test Instructions:**
        1.  Access the deployed frontend URL in a browser.
        2.  Verify the "Hello World" component is displayed.
        3.  Check browser developer tools to ensure assets are loaded from the CDN.

### Epic 1: User Management and Authentication

*   **Story 1.3: Frontend Registration Form**
    *   **Test Instructions:**
        1.  **Display Form:**
            *   Navigate to the registration page.
            *   Verify that input fields for username, email, and password, and a submit button are visible.
        2.  **Successful Registration (E2E):**
            *   Fill in valid registration details.
            *   Click the submit button.
            *   Verify that a success message is displayed or the user is redirected to the login/dashboard page.
            *   (E2E) Verify a new user record exists in the backend.
        3.  **Client-Side Validation:**
            *   Attempt to submit with empty fields.
            *   Attempt to submit with an invalid email format.
            *   Verify appropriate error messages are displayed without a network request.
        4.  **Backend Error Handling:**
            *   (E2E) Attempt to register with a duplicate email.
            *   Verify an error message from the backend is displayed to the user.

*   **Story 1.4: Frontend Login Form**
    *   **Test Instructions:**
        1.  **Display Form:**
            *   Navigate to the login page.
            *   Verify that input fields for email and password, and a submit button are visible.
        2.  **Successful Login (E2E):**
            *   Fill in valid login credentials.
            *   Click the submit button.
            *   Verify the user is redirected to the dashboard or portfolio page.
            *   Verify the JWT token is stored (e.g., in local storage).
        3.  **Client-Side Validation:**
            *   Attempt to submit with empty fields.
            *   Verify appropriate error messages are displayed.
        4.  **Backend Error Handling:**
            *   (E2E) Attempt to log in with incorrect credentials.
            *   Verify an error message from the backend is displayed.

*   **Story 1.5: User Profile Management (Basic)**
    *   **Test Instructions:**
        1.  **Display Profile:**
            *   Log in and navigate to the user profile page.
            *   Verify that the user's current profile information is displayed.
        2.  **Update Profile:**
            *   Modify a profile field (e.g., username).
            *   Click save/update.
            *   Verify a success message is displayed and the updated information is reflected.
            *   (E2E) Verify the change persists after refreshing the page or re-logging in.
        3.  **Error Handling:**
            *   Attempt to submit invalid profile data.
            *   Verify error messages are displayed.

### Epic 2: Portfolio Management and Trading

*   **Story 2.4: Frontend Portfolio Display**
    *   **Test Instructions:**
        1.  **Initial Portfolio View:**
            *   Log in a new user.
            *   Navigate to the portfolio page.
            *   Verify that the initial cash balance ($100,000) is displayed.
            *   Verify that there are no security holdings displayed.
        2.  **Portfolio with Holdings:**
            *   (E2E) Perform some trades via the API or directly manipulate test data.
            *   Log in and navigate to the portfolio page.
            *   Verify that security holdings (symbol, quantity, average cost, current price, unrealized gain/loss) are correctly displayed.
            *   Verify the total portfolio value is accurately calculated and displayed.

*   **Story 2.5: Frontend Trade Form**
    *   **Test Instructions:**
        1.  **Display Form:**
            *   Navigate to the trade page/component.
            *   Verify input fields for symbol, quantity, trade type (buy/sell), and a submit button are visible.
        2.  **Real-time Quote Display:**
            *   Enter a valid stock symbol.
            *   Verify that the current price for that symbol is fetched and displayed.
        3.  **Buy Order (E2E):**
            *   Enter a valid symbol and quantity for a buy order within cash limits.
            *   Click buy.
            *   Verify a success message is displayed.
            *   Verify the portfolio display updates with the new holding and reduced cash.
        4.  **Sell Order (E2E):**
            *   (E2E) Ensure the user has holdings of a security.
            *   Enter a valid symbol and quantity for a sell order within holdings limits.
            *   Click sell.
            *   Verify a success message is displayed.
            *   Verify the portfolio display updates with reduced holdings and increased cash.
        5.  **Insufficient Funds/Shares:**
            *   Attempt a buy order exceeding cash.
            *   Attempt a sell order exceeding shares.
            *   Verify appropriate error messages are displayed to the user.

*   **Story 2.6: Transaction History Display**
    *   **Test Instructions:**
        1.  **Display History:**
            *   Log in and perform several trades.
            *   Navigate to the transaction history page.
            *   Verify that all transactions are listed with correct details (type, symbol, quantity, price, commission, date).
        2.  **Empty History:**
            *   Log in a new user with no trades.
            *   Verify a message indicating no transactions is displayed.

### Epic 3: Rolling Performance Evaluation and Leaderboards

*   **Story 3.4: Frontend Leaderboard Display**
    *   **Test Instructions:**
        1.  **Display Leaderboards:**
            *   Navigate to the leaderboards page.
            *   Verify that tabs/sections for 1-day, 7-day, 30-day, and 90-day leaderboards are visible.
        2.  **Leaderboard Data:**
            *   Select each leaderboard tab.
            *   Verify that a list of users with their PPG and rank is displayed.
            *   Verify the list is sorted correctly by PPG.
        3.  **Empty Leaderboard:**
            *   Test scenario where a leaderboard has no data (e.g., display a message).

