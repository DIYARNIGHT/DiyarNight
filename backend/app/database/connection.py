import os
import motor.motor_asyncio
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import asyncio

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "superonline_smartnet"

# Async MongoDB client for FastAPI
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Collections
users_collection = database.get_collection("users")
addresses_collection = database.get_collection("addresses")
plans_collection = database.get_collection("plans")
usage_collection = database.get_collection("usage")
addons_collection = database.get_collection("addons")
tickets_collection = database.get_collection("tickets")

# Sync client for data loading
sync_client = MongoClient(MONGODB_URL)
sync_database = sync_client[DATABASE_NAME]

async def load_csv_data():
    """Load CSV data into MongoDB collections"""
    try:
        # Clear existing data
        collections = [
            "users", "addresses", "plans", "usage", "addons", "tickets"
        ]
        
        for collection_name in collections:
            await database[collection_name].delete_many({})
        
        # Load CSV files
        csv_files = {
            "users": "users.csv",
            "addresses": "addresses.csv", 
            "plans": "plans.csv",
            "usage": "usage.csv",
            "addons": "addons.csv",
            "tickets": "tickets.csv"
        }
        
        # Go up from backend/app to the root directory where CSV files are
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        for collection_name, csv_file in csv_files.items():
            file_path = os.path.join(base_path, csv_file)
            if os.path.exists(file_path):
                # Try different encodings for Turkish characters
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df = pd.read_csv(file_path, encoding='windows-1254')
                    except UnicodeDecodeError:
                        try:
                            df = pd.read_csv(file_path, encoding='iso-8859-9')
                        except UnicodeDecodeError:
                            df = pd.read_csv(file_path, encoding='latin1')
                
                # Convert DataFrame to dict
                records = df.to_dict('records')
                
                # Special handling for different collections
                if collection_name == "usage":
                    for record in records:
                        record['date'] = pd.to_datetime(record['date']).date().isoformat()
                        
                elif collection_name == "tickets":
                    for record in records:
                        record['created_at'] = pd.to_datetime(record['created_at']).isoformat()
                
                # Insert data
                if records:
                    await database[collection_name].insert_many(records)
                    print(f"Loaded {len(records)} records into {collection_name}")
            else:
                print(f"CSV file not found: {file_path}")
                
        # Add more sample data
        await add_sample_data()
        print("Database initialization completed!")
        
    except Exception as e:
        print(f"Error loading CSV data: {e}")

async def add_sample_data():
    """Add additional comprehensive sample data"""
    try:
        # Add more users with diverse profiles
        sample_users = [
            {"user_id": "U6", "name": "Mehmet Yılmaz", "address_id": "A2", "current_plan_id": "P035", "modem_mac": "00:11:22:33:44:66"},
            {"user_id": "U7", "name": "Fatma Kaya", "address_id": "A3", "current_plan_id": "P200", "modem_mac": "00:11:22:33:44:77"},
            {"user_id": "U8", "name": "Ali Demir", "address_id": "A4", "current_plan_id": "P100", "modem_mac": "00:11:22:33:44:88"},
            {"user_id": "U9", "name": "Zeynep Özkan", "address_id": "A5", "current_plan_id": "P50", "modem_mac": "00:11:22:33:44:99"},
            {"user_id": "U10", "name": "Burak Şen", "address_id": "A6", "current_plan_id": "P1000", "modem_mac": "00:11:22:33:44:AA"}
        ]
        await users_collection.insert_many(sample_users)
        
        # Add more addresses with different characteristics
        sample_addresses = [
            {"address_id": "A8", "city": "İzmir", "district": "Bornova", "fiber": 1, "vdsl": 1, "adsl": 0, "max_speed_mbps": 200},
            {"address_id": "A9", "city": "Bursa", "district": "Nilüfer", "fiber": 0, "vdsl": 1, "adsl": 1, "max_speed_mbps": 100},
            {"address_id": "A10", "city": "Antalya", "district": "Muratpaşa", "fiber": 1, "vdsl": 0, "adsl": 0, "max_speed_mbps": 1000},
            {"address_id": "A11", "city": "Trabzon", "district": "Ortahisar", "fiber": 0, "vdsl": 1, "adsl": 1, "max_speed_mbps": 50},
            {"address_id": "A12", "city": "Eskişehir", "district": "Tepebaşı", "fiber": 1, "vdsl": 1, "adsl": 0, "max_speed_mbps": 500}
        ]
        await addresses_collection.insert_many(sample_addresses)
        
        # Add more comprehensive plans
        sample_plans = [
            {"plan_id": "P025", "name": "Giriş 25", "quota_gb": 150, "speed_mbps": 25, "monthly_price": 299},
            {"plan_id": "P050", "name": "VDSL 50", "quota_gb": 250, "speed_mbps": 50, "monthly_price": 359},
            {"plan_id": "P500", "name": "Fiber 500", "quota_gb": 750, "speed_mbps": 500, "monthly_price": 699},
            {"plan_id": "P1000", "name": "Fiber 1000", "quota_gb": 1000, "speed_mbps": 1000, "monthly_price": 899}
        ]
        await plans_collection.insert_many(sample_plans)
        
        # Add more comprehensive usage data for multiple users and dates
        sample_usage = [
            # U1 - Heavy user
            {"user_id": "U1", "date": "2025-10-07", "used_gb": 22.1},
            {"user_id": "U1", "date": "2025-10-08", "used_gb": 19.8},
            {"user_id": "U1", "date": "2025-09-25", "used_gb": 16.5},
            {"user_id": "U1", "date": "2025-09-26", "used_gb": 14.3},
            
            # U6 - Moderate user
            {"user_id": "U6", "date": "2025-10-01", "used_gb": 5.5},
            {"user_id": "U6", "date": "2025-10-02", "used_gb": 7.2},
            {"user_id": "U6", "date": "2025-10-03", "used_gb": 6.8},
            {"user_id": "U6", "date": "2025-10-04", "used_gb": 4.9},
            
            # U7 - High usage user
            {"user_id": "U7", "date": "2025-10-01", "used_gb": 25.8},
            {"user_id": "U7", "date": "2025-10-02", "used_gb": 28.3},
            {"user_id": "U7", "date": "2025-10-03", "used_gb": 31.2},
            {"user_id": "U7", "date": "2025-10-04", "used_gb": 29.7},
            
            # U8 - Light user
            {"user_id": "U8", "date": "2025-10-01", "used_gb": 2.1},
            {"user_id": "U8", "date": "2025-10-02", "used_gb": 3.4},
            {"user_id": "U8", "date": "2025-10-03", "used_gb": 1.8},
            
            # U9 - Weekend heavy user
            {"user_id": "U9", "date": "2025-10-01", "used_gb": 8.2},
            {"user_id": "U9", "date": "2025-10-02", "used_gb": 12.5},
            
            # U10 - Power user
            {"user_id": "U10", "date": "2025-10-01", "used_gb": 45.2},
            {"user_id": "U10", "date": "2025-10-02", "used_gb": 52.8},
            {"user_id": "U10", "date": "2025-10-03", "used_gb": 48.1}
        ]
        await usage_collection.insert_many(sample_usage)
        
        # Add more addons
        sample_addons = [
            {"addon_id": "A6", "name": "Gaming Paketi", "monthly_price": 149, "description": "Oyun trafiği önceliği"},
            {"addon_id": "A7", "name": "Video Streaming", "monthly_price": 99, "description": "Netflix, YouTube premium"},
            {"addon_id": "A8", "name": "Güvenlik Paketi", "monthly_price": 79, "description": "Antivirüs ve firewall"}
        ]
        await addons_collection.insert_many(sample_addons)
        
        # Add more support tickets
        sample_tickets = [
            {"ticket_id": "T6", "user_id": "U6", "subject": "Hız sorunu", "status": "open", "priority": "medium", "created_date": "2025-10-01"},
            {"ticket_id": "T7", "user_id": "U7", "subject": "Fatura itirazı", "status": "closed", "priority": "low", "created_date": "2025-09-28"},
            {"ticket_id": "T8", "user_id": "U8", "subject": "Modem değişimi", "status": "in_progress", "priority": "high", "created_date": "2025-10-02"},
            {"ticket_id": "T9", "user_id": "U9", "subject": "Bağlantı kesilmesi", "status": "open", "priority": "high", "created_date": "2025-10-02"}
        ]
        await tickets_collection.insert_many(sample_tickets)
        
        print("✅ Additional sample data added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")

async def get_database():
    return database