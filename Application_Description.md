# **Product Design Description:**

# **Hive Investor Individual Investment Simulator**

**Objective:** To design a web application that provides a persistent, individual-focused, and continuously evaluated stock market simulation experience, enabling self-paced financial literacy development.

## **1\. Product Overview and Goal**

Product Name: HiveInvestor  
Mission: To provide individuals with an accessible, risk-free environment to practice active investing with real-world market data, tracked through continuous, rolling performance metrics.  
HiveInvestor is fundamentally a simulation derived from the core mechanics of the SMG (virtual capital, real-time data, security types) but adapted for a persistent, non-classroom user base. The primary differentiation lies in the removal of fixed competition windows and team structures, favoring individual, continuous portfolio management.

## **2\. Target Audience and Core Use Case**

**Primary Target Audience:** Individual retail investors and students (16+) seeking practical, self-directed experience with financial markets outside of a formal curriculum.

**Core Use Case:** A user signs up at any time, receives virtual capital, and manages a persistent portfolio of stocks, bonds, and mutual funds. Their success is evaluated against all other players based on how well their portfolio performs over rolling 30-day and 90-day periods.

## **3\. Key Features (MVP Focus)**

The design must satisfy the three core user requirements that differentiate it from the traditional SMG:

### **3.1. Individual, Self-Paced Participation**

* **User Model:** Accounts are strictly individual. No team setup is required or permitted.
* **Continuous Enrollment:** New players can register and start their simulation instantly, 24/7/365. There are no fixed start dates or seasons.
* **Persistent Portfolios:** Once a player starts, their portfolio and transaction history are maintained indefinitely. Players may reset their portfolio, but the system will track their history before the reset.

### **3.2. Rolling Performance Evaluation**

This is the most critical difference and addresses the need for continuous competition and evaluation.

* **Primary Metric:** **Percentage Portfolio Gain (PPG)**. Calculated based on the total net portfolio value (cash \+ security value) relative to the value at the start of the evaluation period.
* **Evaluation Windows (Rolling Leaderboards):**
    1. **1-Day PPG Leaderboard:** Performance over the last 24 hours.
    2. **7-Day PPG Leaderboard:** Performance over the last 7 calendar days.
    2. **30-Day PPG Leaderboard:** Performance over the last 30 calendar days.
    3. **90-Day PPG Leaderboard:** Performance over the last 90 calendar days (Quarterly proxy).
* **Logic:** The system continuously recalculates the PPG for all active users daily and updates the leaderboards. This allows a new player to immediately compete based on their first 7, 30, or 90 days, or for a veteran player to compete based on their most recent performance.

## **4\. Core Functional Requirements **

| Feature | Description | Implementation Detail |
| :---- | :---- | :---- |
| **Initial Capital** | Each new portfolio starts with $\\$100,000$ in virtual cash. | Fixed, non-negotiable starting amount. |
| **Security Types** | Trading access to common stocks, mutual funds, and corporate/government bonds. | Integration with a real-time market data API. |
| **Real-Time Data** | Security prices and portfolio valuation updated in real-time (with typical 15-20 min educational delay). | API integration for stock quotes and market news. |
| **Transaction Rules** | Standard commission/transaction fees must be applied (e.g., $\\$10$ flat commission per trade) to mirror real-world costs. | Portfolio value calculation must subtract fees. |
| **Reporting** | Portfolio Summary (Current Value, Cash Balance, Unrealized Gain/Loss), Transaction History. | Persistent storage in Firestore, updated upon trade execution. |

## 


