# Code Development with Google Gemini CLI
[The Doc](https://docs.google.com/document/d/1zi3tl4cEmJHUvnpiMrOUyxY8ljPJP5I6ZcLy13X0HWk/edit?tab=t.0#heading=h.i7bj66vab6d1)


# HiveInvestor: Individual Investment Simulator

## Project Overview

HiveInvestor is a web application designed to provide a persistent, individual-focused, and continuously evaluated stock market simulation experience. Its mission is to offer individuals an accessible, risk-free environment to practice active investing with real-world market data, tracked through continuous, rolling performance metrics.

This platform is adapted from traditional stock market games but removes fixed competition windows and team structures, favoring individual, continuous portfolio management.

## Key Features (MVP Focus)

### Individual, Self-Paced Participation
*   **User Model:** Accounts are strictly individual. No team setup is required or permitted.
*   **Continuous Enrollment:** New players can register and start their simulation instantly, 24/7/365. There are no fixed start dates or seasons.
*   **Persistent Portfolios:** Once a player starts, their portfolio and transaction history are maintained indefinitely. Players may reset their portfolio, but the system will track their history before the reset.

### Rolling Performance Evaluation
This is the most critical difference and addresses the need for continuous competition and evaluation.
*   **Primary Metric:** **Percentage Portfolio Gain (PPG)**. Calculated based on the total net portfolio value (cash + security value) relative to the value at the start of the evaluation period.
*   **Evaluation Windows (Rolling Leaderboards):**
    1.  **1-Day PPG Leaderboard:** Performance over the last 24 hours.
    2.  **7-Day PPG Leaderboard:** Performance over the last 7 calendar days.
    3.  **30-Day PPG Leaderboard:** Performance over the last 30 calendar days.
    4.  **90-Day PPG Leaderboard:** Performance over the last 90 calendar days (Quarterly proxy).
*   **Logic:** The system continuously recalculates the PPG for all active users daily and updates the leaderboards. This allows a new player to immediately compete based on their first 7, 30, or 90 days, or for a veteran player to compete based on their most recent performance.

## Local Development Setup

To set up your local development environment, please refer to the comprehensive [Local Development Guide](context/LocalDevGuide.md). This guide provides detailed instructions for setting up VirtualBox, Vagrant, Python (FastAPI) for the backend, and Node.js (Vue.js with Tailwind CSS) for the frontend on a macOS host.

## Documentation

*   **Technical Design Document:** [context/TechnicalDesign.md](context/TechnicalDesign.md)
*   **Deployment Guide:** [context/Deployment.md](context/Deployment.md)
*   **Development Plan:** [context/DevelopmentPlan.md](context/DevelopmentPlan.md)
*   **Backend Testing Plan:** [context/testing/BackEndTestPlan.md](context/testing/BackEndTestPlan.md)
*   **Frontend Testing Plan:** [context/testing/FrontEndTestPlan.md](context/testing/FrontEndTestPlan.md)
