# ✈️ Flight Deals Tracker

A Python application that searches for the lowest flight prices using the Amadeus API and automatically updates a Google Sheet via the Sheety API.

This project was built to practice API integration, authentication handling, date manipulation, and clean project structure.

---

## 🚀 Features

- OAuth2 authentication with Amadeus API  
- Automatic IATA code lookup for cities  
- Smart generation of last-day-of-month search dates  
- Lowest price search across multiple months  
- Automatic Google Sheets update via Sheety API  
- Token caching with expiration handling  

---

## 🛠 Technologies Used

- Python 3  
- Requests  
- Amadeus Flight Offers API  
- Sheety API  
- python-dotenv  

---

## 📂 Project Structure

```
flight-deals-tracker/
│
├── main.py
├── flight_data.py
├── flight_search.py
├── config.env
└── README.md
```

---

## ⚙️ How It Works

1. The application loads environment variables (API keys).  
2. It checks the Google Sheet for missing IATA codes.  
3. If missing, it queries the Amadeus API to retrieve them.  
4. It generates search dates based on user input (months ahead).  
5. It searches for the lowest available flight price from the origin city.  
6. It updates the Google Sheet automatically.  

**Note:** You need to set your origin city in `main.py` (default is Iata: LOS - Aeroporto Internacional Murtala Muhammed) or update it to your preferred departure airport.  


---

## 🎬 Full Application Workflow

This demonstration shows the complete system flow:

- User selects how many months ahead to search
- Missing IATA codes are automatically retrieved
- Lowest flight prices are searched via Amadeus API
- Google Sheet is automatically updated

![Example.gif](Assets/Example.gif)
---

## 🔑 Environment Variables

Create a file named `config.env` in the root directory:

```
AMADEUS_API_KEY=your_api_key
AMADEUS_API_SECRET=your_api_secret
DATA_SHEETY_TOKEN=your_sheety_token
```

---

## ▶️ How to Run

Install dependencies:

```
pip install requests python-dotenv
```

Run the application:

```
python main.py
```

Then enter how many months ahead you want to search.

---

## 🧩 Future Improvements

- Add logging instead of print statements  
- Improve API error handling  
- Add email notifications for price drops  
- Convert into a scheduled background service  
- Dockerize the application  

---

## 📌 Purpose

This project was created for learning and portfolio purposes, focusing on:

- Clean code structure  
- API integration  
- Authentication management  
- Real-world automation workflows  

---

## 👨‍💻 Author

Bruno Henrique Domingos  
Python Developer | Systems Analyst  
