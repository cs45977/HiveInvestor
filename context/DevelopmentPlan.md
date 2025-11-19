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
    *   **Status:** Not Started

*   **Story 0.5: GCP Cloud Storage/CDN Deployment for Frontend**
    *   **Description:** Configure Google Cloud Storage and Cloud CDN to host and serve the Vue.js "Hello World" frontend.
    *   **Status:** Not Started

*   **Story 0.6: Basic CI/CD Pipeline (Cloud Build)**
    *   **Description:** Implement a basic CI/CD pipeline using Cloud Build to automate the build and deployment of both frontend and backend "Hello World" applications.
    *   **Status:** Not Started

## Epic 1: User Management and Authentication
**Objective:** Enable users to register, log in, and manage their basic profiles.

### Stories:

*   **Story 1.1: User Registration API Endpoint**
    *   **Description:** Implement a FastAPI endpoint for user registration, including password hashing and storage in Firestore.
    *   **Status:** Not Started

*   **Story 1.2: User Login API Endpoint (JWT)**
    *   **Description:** Implement a FastAPI endpoint for user login, generating and returning a JWT upon successful authentication.
    *   **Status:** Not Started

*   **Story 1.3: Frontend Registration Form**
    *   **Description:** Create a Vue.js component for user registration, interacting with the backend API.
    *   **Status:** Not Started

*   **Story 1.4: Frontend Login Form**
    *   **Description:** Create a Vue.js component for user login, handling JWT storage and redirection upon successful login.
    *   **Status:** Not Started

*   **Story 1.5: User Profile Management (Basic)**
    *   **Description:** Implement API endpoints and frontend components for users to view and update basic profile information.
    *   **Status:** Not Started

## Epic 2: Portfolio Management and Trading
**Objective:** Allow users to create and manage their investment portfolios, including buying and selling securities.

### Stories:

*   **Story 2.1: Portfolio Initialization API**
    *   **Description:** Implement a FastAPI endpoint to initialize a new user's portfolio with $100,000 virtual cash.
    *   **Status:** Not Started

*   **Story 2.2: External Market Data API Integration**
    *   **Description:** Integrate a third-party market data API to fetch real-time security quotes.
    *   **Status:** Not Started

*   **Story 2.3: Buy/Sell Trade API Endpoint**
    *   **Description:** Implement FastAPI endpoints for executing buy and sell orders, including validation, commission calculation, and portfolio updates.
    *   **Status:** Not Started

*   **Story 2.4: Frontend Portfolio Display**
    *   **Description:** Create Vue.js components to display the user's current portfolio holdings, cash balance, and total value.
    *   **Status:** Not Started

*   **Story 2.5: Frontend Trade Form**
    *   **Description:** Create a Vue.js component for users to input and execute buy/sell orders.
    *   **Status:** Not Started

*   **Story 2.6: Transaction History Display**
    *   **Description:** Implement API endpoints and frontend components to display a user's transaction history.
    *   **Status:** Not Started

## Epic 3: Rolling Performance Evaluation and Leaderboards
**Objective:** Implement the core logic for continuous portfolio evaluation and display rolling leaderboards.

### Stories:

*   **Story 3.1: PPG Calculation Logic**
    *   **Description:** Develop the backend logic for calculating Percentage Portfolio Gain (PPG) for individual portfolios over various timeframes.
    *   **Status:** Not Started

*   **Story 3.2: Scheduled Portfolio Evaluation (Cloud Functions/Cloud Run Jobs)**
    *   **Description:** Implement a scheduled GCP service (Cloud Functions or Cloud Run Jobs) to periodically recalculate PPG for all active users.
    *   **Status:** Not Started

*   **Story 3.3: Leaderboard API Endpoints**
    *   **Description:** Implement FastAPI endpoints to retrieve 1-day, 7-day, 30-day, and 90-day PPG leaderboards.
    *   **Status:** Not Started

*   **Story 3.4: Frontend Leaderboard Display**
    *   **Description:** Create Vue.js components to display the various rolling leaderboards.
    *   **Status:** Not Started

## Epic 4: Documentation and Testing Plans
**Objective:** Create comprehensive documentation for local development, deployment, and testing.

### Stories:

*   **Story 4.1: Local Development Guide**
    *   **Description:** Create a detailed guide for setting up the local development environment for both frontend and backend.
    *   **Status:** Not Started

*   **Story 4.2: Deployment Guide**
    *   **Description:** Create a comprehensive guide for deploying the HiveInvestor application to Google Cloud Platform.
    *   **Status:** Not Started

*   **Story 4.3: Backend Testing Plan**
    *   **Description:** Create a document outlining the testing strategy and specific test cases for the FastAPI backend.
    *   **Status:** Not Started

*   **Story 4.4: Frontend Testing Plan**
    *   **Description:** Create a document outlining the testing strategy and specific test cases for the Vue.js frontend.
    *   **Status:** Not Started
