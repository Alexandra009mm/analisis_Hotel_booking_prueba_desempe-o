# Data Engineering Project — ETL, Database & Business Intelligence

## 1. Project Overview

### Project Name
`Hotel Booking Demand`

### Domain
`Hotels`

### Objective
The objective of this project is to develop an end-to-end data pipeline that extracts data from a public source, transforms and validates the information using Python and Pandas, stores the processed data in PostgreSQL, and finally uses Power BI to generate business insights.

The project follows the following workflow:

```text
Data Source
    ↓
Extraction
    ↓
Transformation
    ↓
Validation
    ↓
PostgreSQL
    ↓
Data Model
    ↓
Power BI
    ↓
Business Insights
```

---

## 2. Project Objectives

### General Objective
`ANSWER ANY QUESTIONS ABOUT THE DATASET`

### Specific Objectives
* Extract data from `KAGGLE.COM - https://kaggle.com`.
* Analyze the initial data structure and quality.
* Clean and transform the dataset using Pandas and functions.
* Apply data quality validations.
* Design an appropriate database model.
* Load the transformed data into PostgreSQL.
* Connect PostgreSQL to Power BI.
* Create analytical measures and visualizations.
* Answer relevant business questions.
* Generate actionable insights from the data.

---

## 3. Data Source

### 3.1 Source Information
* **Source:** `Kaggle/CSV`
* **Dataset:** `hotel_bookings.csv`
* **URL:** `https://kaggle.com`
* **Rows:** `119,390`
* **Columns:** `32`

---

### 3.2 Dataset Description
The dataset contains information related to:

| # | Column | Data Type | Description |
|---|---|---|---|
| 1 | hotel | Categorical | Type of hotel: City Hotel or Resort Hotel. |
| 2 | is_canceled | Binary | Indicates whether the reservation was canceled. 1 = canceled, 0 = not canceled. |
| 3 | lead_time | Integer | Number of days between the booking date and the arrival date. |
| 4 | arrival_date_year | Integer | Year of the planned arrival date. |
| 5 | arrival_date_month | Categorical | Month of the planned arrival date. |
| 6 | arrival_date_week_number | Integer | Week number of the planned arrival date. |
| 7 | arrival_date_day_of_month | Integer | Day of the month of the planned arrival date. |
| 8 | stays_in_weekend_nights | Integer | Number of weekend nights included in the reservation. |
| 9 | stays_in_week_nights | Integer | Number of weekday nights included in the reservation. |
| 10 | adults | Integer | Number of adults included in the reservation. |
| 11 | children | Float | Number of children included in the reservation. |
| 12 | babies | Integer | Number of babies included in the reservation. |
| 13 | meal | Categorical | Meal plan associated with the reservation. |
| 14 | country | Categorical | Country of origin of the guest. |
| 15 | market_segment | Categorical | Market segment associated with the reservation. |
| 16 | distribution_channel | Categorical | Distribution channel through which the reservation was made. |
| 17 | is_repeated_guest | Binary | Indicates whether the guest is a returning customer. 1 = repeated guest, 0 = new guest. |
| 18 | previous_cancellations | Integer | Number of previous reservations canceled by the guest. |
| 19 | previous_bookings_not_canceled | Integer | Number of previous reservations that were not canceled. |
| 20 | reserved_room_type | Categorical | Room type originally requested by the guest. |
| 21 | assigned_room_type | Categorical | Room type finally assigned to the guest. |
| 22 | booking_changes | Integer | Number of changes made to the reservation. |
| 23 | deposit_type | Categorical | Type of deposit associated with the reservation. |
| 24 | agent | Identifier | ID of the travel agency associated with the reservation. |
| 25 | company | Identifier | ID of the company associated with the reservation. |
| 26 | days_in_waiting_list | Integer | Number of days the reservation remained on the waiting list. |
| 27 | customer_type | Categorical | Type of customer associated with the reservation. |
| 28 | adr | Float | Average Daily Rate charged for the reservation. |
| 29 | required_car_parking_spaces | Integer | Number of parking spaces requested by the guest. |
| 30 | total_of_special_requests | Integer | Total number of special requests made by the guest. |
| 31 | reservation_status | Categorical | Final status of the reservation: Check-Out, Canceled, or No-Show. |
| 32 | reservation_status_date | Date | Date when the final reservation status was recorded. |

---

### 3.3 Dataset Selection Justification

#### Why was this dataset selected?
The Hotel Booking dataset was selected because it contains detailed information about hotel reservations, customer characteristics, booking behavior, room types, prices, cancellations, and reservation outcomes.

This dataset is appropriate for the project because it provides enough information to implement a complete data engineering pipeline, including data extraction, cleaning, transformation, validation, relational modeling, and business intelligence analysis.

The dataset was considered appropriate because it contains:
* **Temporal information:** Arrival year, arrival month, arrival week, arrival day, and reservation status date.
* **Categorical information:** Hotel type, meal plan, country, market segment, distribution channel, room type, deposit type, and customer type.
* **Numerical information:** Lead time, number of guests, length of stay, ADR, booking changes, previous cancellations, and special requests.
* **Business-relevant information:** Reservation cancellations, customer type, booking channels, room assignments, pricing, and reservation status.

These characteristics allow the development of meaningful analytical questions related to hotel performance, customer behavior, cancellations, pricing, and booking patterns.

---

## 4. Business Context

### 4.1 Business Problem
Hotels need to understand their reservation patterns and customer behavior in order to make better operational and commercial decisions.

The dataset contains information about reservations, cancellations, customer characteristics, booking channels, room types, length of stay, and daily rates. However, this information must be cleaned, structured, and analyzed before it can be used effectively for decision-making.

The main business problem is to identify patterns in hotel reservations and cancellations and understand which factors may influence booking behavior and hotel performance.

The analysis will focus on questions such as:
* How does the number of reservations change over time?
* What is the cancellation rate for each hotel type?
* Which market segments generate the most reservations?
* How does the average daily rate (ADR) change over time?
* Is there a relationship between lead time and reservation cancellations?
* Which customer types have the highest cancellation rates?
* Which room types are most frequently requested?

The final objective is to transform the raw reservation data into reliable and structured information that can be used in PostgreSQL and Power BI to generate actionable business insights.

### 4.2 Stakeholder
**Stakeholder:** `MARKETING AND FINANCES`

The main stakeholder needs information about:
* `[NEED 1]`
* `[NEED 2]`
* `[NEED 3]`

---

## 5. Installation and Execution

Follow these steps to set up the virtual environment, environment variables, and run the application correctly.

### 5.1 Prerequisites
* **Python 3.x** installed.
* **Node.js** installed.
* **PostgreSQL** installed and running.

### 5.2 Virtual Environment Configuration (Python)
1. Create a virtual environment in the project root directory:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   * **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   * **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
3. Install the required Python dependencies for the ETL process:
   ```bash
   pip install -r requirements.txt
   ```

### 5.3 Environment Variables Configuration (.env)
1. Duplicate the template file to create your local configuration:
   ```bash
   cp env.example .env
   ```
2. Open the newly created `.env` file and configure your database credentials.
3. **PostgreSQL Port Note:** 
   * By default, this project connects via port **`5433`**.
   * If your PostgreSQL server runs on the standard port or is deployed on other machines across your network, change the port to **`5432`** accordingly.

*Example configuration in the `.env` file:*
```env
DB_HOST=localhost
DB_PORT=5433  # Change to 5432 on machines using the standard PostgreSQL port
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=Hotel Booking Demand
```

### 5.4 Execution (Node.js)
Once you have verified that all libraries in your virtual environment are successfully installed and the credentials in your `.env` file are accurate, install the Node.js packages and run the main entry point:

```bash
npm install
node src/main.js
```
