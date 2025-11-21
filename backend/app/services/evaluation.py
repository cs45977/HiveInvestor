import asyncio
from google.cloud import firestore
from datetime import datetime, date, timezone
from app.services.market_data import get_real_time_quote
from app.models.snapshot import PortfolioSnapshot
from app.models.portfolio import PortfolioInDB # For type hinting portfolio data
from typing import List, Dict

async def snapshot_portfolio(db, user_id: str):
    """
    Calculates the current value of a user's portfolio and saves it as a snapshot.
    """
    today_date_str = date.today().isoformat()
    snapshot_doc_id = f"{user_id}_{today_date_str}"
    
    # Check if snapshot already exists for today
    if db.collection("portfolio_snapshots").document(snapshot_doc_id).get().exists:
        print(f"Snapshot for user {user_id} already exists for {today_date_str}. Skipping.")
        return

    portfolio_ref = db.collection("portfolios").document(user_id)
    portfolio_doc = portfolio_ref.get()

    if not portfolio_doc.exists:
        print(f"Portfolio not found for user {user_id}. Skipping snapshot.")
        return

    portfolio_data = portfolio_doc.to_dict()
    
    current_cash_balance = portfolio_data.get("cash_balance", 0.0)
    holdings = portfolio_data.get("holdings", [])
    
    holdings_value = 0.0
    quote_tasks = []
    
    # Fetch market prices for all holdings concurrently
    for holding in holdings:
        quote_tasks.append(get_real_time_quote(holding["symbol"]))
    
    quotes = await asyncio.gather(*quote_tasks, return_exceptions=True) # Gather results, handle exceptions
    
    for i, holding in enumerate(holdings):
        quote = quotes[i]
        market_price = 0.0
        if isinstance(quote, Exception):
            print(f"Error fetching quote for {holding['symbol']}: {quote}")
        else:
            market_price = quote.price
        
        holdings_value += holding["quantity"] * market_price

    calculated_total_value = current_cash_balance + holdings_value
    
    new_snapshot = PortfolioSnapshot(
        user_id=user_id,
        date=today_date_str,
        total_value=round(calculated_total_value, 2),
        timestamp=datetime.now(timezone.utc)
    )
    
    db.collection("portfolio_snapshots").document(snapshot_doc_id).set(new_snapshot.model_dump())
    print(f"Snapshot created for user {user_id} for {today_date_str} with value {calculated_total_value}")

def calculate_ppg(current_value: float, start_value: float) -> float:
    """
    Calculates Percentage Portfolio Gain (PPG).
    """
    if start_value == 0:
        return 0.0
    return ((current_value - start_value) / start_value) * 100.0

async def update_all_portfolios_total_value(db):
    """
    Recalculates total_value for all portfolios based on current market prices
    and triggers a snapshot for each.
    """
    users_ref = db.collection("users")
    all_users = users_ref.stream()

    for user_doc in all_users:
        user_id = user_doc.id
        portfolio_ref = db.collection("portfolios").document(user_id)
        portfolio_doc = portfolio_ref.get()

        if not portfolio_doc.exists:
            print(f"Portfolio not found for user {user_id}. Skipping total value update.")
            continue

        portfolio_data = portfolio_doc.to_dict()
        current_cash_balance = portfolio_data.get("cash_balance", 0.0)
        holdings = portfolio_data.get("holdings", [])

        holdings_value = 0.0
        quote_tasks = []
        for holding in holdings:
            quote_tasks.append(get_real_time_quote(holding["symbol"]))

        quotes = await asyncio.gather(*quote_tasks, return_exceptions=True)

        for i, holding in enumerate(holdings):
            quote = quotes[i]
            market_price = 0.0
            if isinstance(quote, Exception):
                print(f"Error fetching quote for {holding['symbol']}: {quote}")
            else:
                market_price = quote.price
            
            holdings_value += holding["quantity"] * market_price
        
        calculated_total_value = current_cash_balance + holdings_value
        
        # Update portfolio's total_value field
        portfolio_ref.update({"total_value": round(calculated_total_value, 2)})
        print(f"Updated total_value for user {user_id} to {calculated_total_value}")

        # Take a snapshot
        await snapshot_portfolio(db, user_id)

from datetime import timedelta
from app.models.leaderboard import Leaderboard, LeaderboardEntry

async def generate_leaderboards(db):
    """
    Generates and updates leaderboards for various time windows.
    """
    windows = {
        "1d": 1,
        "7d": 7,
        "30d": 30,
        "90d": 90
    }
    
    users_ref = db.collection("users")
    users = [doc for doc in users_ref.stream()]
    
    today = date.today()
    today_str = today.isoformat()
    
    for window_name, days in windows.items():
        start_date_str = (today - timedelta(days=days)).isoformat()
        entries = []
        
        for user_doc in users:
            user_id = user_doc.id
            user_data = user_doc.to_dict()
            username = user_data.get("username", "Unknown")
            
            today_snap_ref = db.collection("portfolio_snapshots").document(f"{user_id}_{today_str}")
            start_snap_ref = db.collection("portfolio_snapshots").document(f"{user_id}_{start_date_str}")
            
            today_snap = today_snap_ref.get()
            start_snap = start_snap_ref.get()
            
            if today_snap.exists and start_snap.exists:
                current_value = today_snap.to_dict().get("total_value", 0.0)
                start_value = start_snap.to_dict().get("total_value", 0.0)
                
                ppg = calculate_ppg(current_value, start_value)
                
                entries.append(LeaderboardEntry(
                    user_id=user_id,
                    username=username,
                    ppg=round(ppg, 2),
                    rank=0 
                ))
        
        entries.sort(key=lambda x: x.ppg, reverse=True)
        
        for i, entry in enumerate(entries):
            entry.rank = i + 1
            
        leaderboard = Leaderboard(
            id=window_name,
            updated_at=datetime.now(timezone.utc),
            entries=entries
        )
        
        db.collection("leaderboards").document(window_name).set(leaderboard.model_dump())
        print(f"Updated {window_name} leaderboard with {len(entries)} entries.")
