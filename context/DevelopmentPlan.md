# Development Plan: HiveInvestor

This development plan outlines the epics and stories for building the HiveInvestor application, following a FastAPI backend, Vue.js frontend, and Google Cloud Platform deployment strategy. Each story will include its current status.

## Epic 0: Setup and "Hello World" Deployment
**Objective:** Establish the basic development environment, scaffold the frontend and backend, and deploy a minimal "Hello World" application to GCP to validate the CI/CD pipeline and deployment process.

### Stories:

*   **Story 0.1: Backend Project Initialization (FastAPI)**
    *   **Description:** Initialize a new FastAPI project, set up basic project structure, and create a simple "Hello World" endpoint.
    *   **Status:** Complete

*   **Story 0.2: Frontend Project Initialization (Vue.js with Tailwind CSS)**
    *   **Description:** Initialize a new Vue.js project, integrate Tailwind CSS, and create a simple "Hello World" component.
    *   **Status:** Complete

*   **Story 0.3: Dockerization of Backend and Frontend**
    *   **Description:** Create Dockerfiles for both the FastAPI backend and the Vue.js frontend to enable containerized deployment.
    *   **Status:** Complete

*   **Story 0.4: GCP Project Setup and Cloud Run Deployment for Backend**
    *   **Description:** Set up a GCP project, configure Cloud Run for the FastAPI backend, and deploy the "Hello World" endpoint.
    *   **Status:** Complete

*   **Story 0.5: GCP Cloud Storage/CDN Deployment for Frontend**
    *   **Description:** Configure Google Cloud Storage and Cloud CDN to host and serve the Vue.js "Hello World" frontend.
    *   **Status:** Complete

*   **Story 0.6: Basic CI/CD Pipeline (Cloud Build)**
    *   **Description:** Implement a basic CI/CD pipeline using Cloud Build to automate the build and deployment of both frontend and backend "Hello World" applications.
    *   **Status:** Complete

*   **Story 0.7: Frontend to Backend Communication**
    *   **Description:** Implement a simple API call from the Vue.js frontend to the FastAPI backend to ensure both are being served correctly and can communicate. This includes a visual and textual indicator on the frontend that shows the status of the backend connection, using humorous messages and GIFs for success and error states.
    *   **Status:** Complete

*   **Story 0.8: Set up Unit Testing Frameworks**
    *   **Description:** Install and configure unit testing frameworks for both the frontend (Vitest) and backend (Pytest). Create an initial example test for both to ensure the testing pipeline is functional.
    *   **Status:** Complete

*   **Story 0.9: Enhanced Backend and Database Connection Check**
    *   **Description:** Improve the backend health check endpoint to verify connectivity with the Firestore database. Update the frontend to display detailed status indicators for both the backend service and the database connection, distinguishing between development and production environments.
    *   **Status:** Complete

*   **Story 0.10: Local Testing Database Setup (Firestore Emulator)**
    *   **Description:** Set up the Firestore Emulator in the local development environment to serve as a testing database. Ensure the backend connects to this local emulator when running in development mode. Update the Local Development Guide with instructions for running the emulator.
    *   **Status:** Complete

## Epic 1: User Management and Authentication
**Objective:** Enable users to register, log in, and manage their basic profiles.

### Stories:

*   **Story 1.1: User Registration API Endpoint**
    *   **Description:** Following a test-first TDD approach, write failing unit tests that define the requirements for a user registration endpoint. Then, implement the FastAPI endpoint to make the tests pass, including password hashing and storage in Firestore.
    *   **Status:** Complete

*   **Story 1.2: User Login API Endpoint (JWT)**
    *   **Description:** Implement a FastAPI endpoint for user login, generating and returning a JWT upon successful authentication.
    *   **Status:** Complete

*   **Story 1.3: Frontend Registration Form**
    *   **Description:** Following a test-first TDD approach, write failing component tests that define the behavior of a user registration form. Then, create the Vue.js component to make the tests pass, ensuring it interacts correctly with the backend API.
    *   **Status:** Complete

*   **Story 1.4: Frontend Login Form**
    *   **Description:** Create a Vue.js component for user login, handling JWT storage and redirection upon successful login.
    *   **Status:** Complete

*   **Story 1.5: User Profile Management (Basic)**
    *   **Description:** Implement API endpoints and frontend components for users to view and update basic profile information.
    *   **Status:** Complete

## Epic 2: Portfolio Management and Trading
**Objective:** Allow users to create and manage their investment portfolios, including buying and selling securities.

### Stories:

*   **Story 2.1: Portfolio Initialization API**
    *   **Description:** Implement a FastAPI endpoint to initialize a new user's portfolio with $100,000 virtual cash.
    *   **Status:** Complete

*   **Story 2.2: External Market Data API Integration**
    *   **Description:** Integrate a third-party market data API to fetch real-time security quotes.
    *   **Status:** Complete

*   **Story 2.3: Buy/Sell Trade API Endpoint**
    *   **Description:** Implement FastAPI endpoints for executing buy and sell orders, including validation, commission calculation, and portfolio updates.
    *   **Status:** Complete

*   **Story 2.4: Frontend Portfolio Display**
    *   **Description:** Create Vue.js components to display the user's current portfolio holdings, cash balance, and total value.
    *   **Status:** Complete

*   **Story 2.5: Frontend Trade Form**
    *   **Description:** Create a Vue.js component for users to input and execute buy/sell orders.
    *   **Status:** Complete

*   **Story 2.6: Transaction History Display**
    *   **Description:** Implement API endpoints and frontend components to display a user's transaction history.
    *   **Status:** Complete

## Epic 3: Rolling Performance Evaluation and Leaderboards
**Objective:** Implement the core logic for continuous portfolio evaluation and display rolling leaderboards.

### Stories:

*   **Story 3.1: PPG Calculation Logic**
    *   **Description:** Develop the backend logic for calculating Percentage Portfolio Gain (PPG) for individual portfolios over various timeframes.
    *   **Status:** Complete

*   **Story 3.2: Scheduled Portfolio Evaluation (Cloud Functions/Cloud Run Jobs)**
    *   **Description:** Implement a scheduled GCP service (Cloud Functions or Cloud Run Jobs) to periodically recalculate PPG for all active users.
    *   **Status:** Complete (Implemented as Admin API triggerable by Scheduler)

*   **Story 3.3: Leaderboard API Endpoints**
    *   **Description:** Implement FastAPI endpoints to retrieve 1-day, 7-day, 30-day, and 90-day PPG leaderboards.
    *   **Status:** Complete

*   **Story 3.4: Frontend Leaderboard Display**
    *   **Description:** Create Vue.js components to display the various rolling leaderboards.
    *   **Status:** Complete

## Epic 4: Documentation and Testing Plans
**Objective:** Create comprehensive documentation for local development, deployment, and testing.

### Stories:

*   **Story 4.1: Local Development Guide**
    *   **Description:** Create a detailed guide for setting up the local development environment for both frontend and backend.
    *   **Status:** Complete

*   **Story 4.2: Deployment Guide**
    *   **Description:** Create a comprehensive guide for deploying the HiveInvestor application to Google Cloud Platform.
    *   **Status:** Complete

*   **Story 4.3: Backend Testing Plan**
    *   **Description:** Create a document outlining the testing strategy and specific test cases for the FastAPI backend.
    *   **Status:** Complete

*   **Story 4.4: Frontend Testing Plan**
    *   **Description:** Create a document outlining the testing strategy and specific test cases for the Vue.js frontend.
    *   **Status:** Complete

## Epic 5: Advanced Research and Trading Interface
**Objective:** Implement a professional-grade trading interface with advanced charting, real-time data analysis, and sophisticated order entry capabilities.

### Stories:

*   **Story 5.1: Unified Research & Order Entry Layout**
    *   **Description:** Refactor the Trade page to use a split-pane layout (Research Panel / Order Entry Panel) responsive for desktop and mobile.
    *   **Status:** Complete

*   **Story 5.2: Enhanced Quote Header**
    *   **Description:** Implement a component to display real-time quote data including LTP, Change, % Change, Day's High/Low, 52w High/Low, Volume, and Open. Connect to market data service.
    *   **Status:** Complete

*   **Story 5.3: Interactive Charting Component**
    *   **Description:** Integrate a charting library (e.g., Lightweight Charts) to display interactive candlestick/line charts with timeframe selection (1D-MAX) and basic technical indicators.
    *   **Status:** Complete

*   **Story 5.4: Limit Order Support (Backend)**
    *   **Description:** Update `Trade` model and `POST /api/v1/trade` endpoint to accept `order_type` (MARKET, LIMIT) and `limit_price`. Implement validation logic for limit orders.
    *   **Status:** Complete

*   **Story 5.5: Enhanced Order Entry Form (Frontend)**
    *   **Description:** Upgrade the frontend trade form to support Buy/Sell toggle, Market/Limit selection, conditional limit price input, and dynamic quantity selectors (25%, 50%, 100%).
    *   **Status:** Complete

*   **Story 5.6: Time in Force (TIF) Support**
    *   **Description:** Add `time_in_force` (DAY, GTC) to backend trade model and frontend form. Implement expiration logic for DAY orders (scheduled job or check-on-access).
    *   **Status:** Complete (Data support & validation implemented. Expiration logic deferred as per MVP scope).

*   **Story 5.7: Trade Confirmation Modal**
    *   **Description:** Implement a confirmation modal that summarizes the trade (Estimated Cost/Revenue) before final submission.
    *   **Status:** Complete
