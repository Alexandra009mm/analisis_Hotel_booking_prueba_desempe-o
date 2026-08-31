import pandas as pd

from utils import (
    column_normalization,
    clean_text_spaces,
    data_type_conversion,
    handle_nulls,
)


dataType_list = {
    "is_canceled": "bool",
    "lead_time": "int64",
    "booking_changes": "int64",
    "adults": "int64",
    "children": "int64",
    "babies": "int64",
    "adr": "float64",
    "required_car_parking_spaces": "int64",
    "total_of_special_requests": "int64",
    "previous_cancellations": "int64",
    "previous_bookings_not_canceled": "int64",
    "stays_in_weekend_nights": "int64",
    "stays_in_week_nights": "int64",
    "days_in_waiting_list": "int64",
}

strategy = {
    "is_canceled": 0,
    "children": 0,
    "babies": 0,
    "agent": 0,
    "company": 0,
    "country": "Unknown",
}


def transform_data(df: pd.DataFrame):
    """Apply the existing cleaning functions to the raw DataFrame."""
    print("\n[=== STARTING DATA TRANSFORMATION ===]\n")

    df = df.copy()

    print("Step 1/4: Normalizing column names...")
    df = column_normalization(df)

    print("Step 2/4: Cleaning text spaces...")
    df = clean_text_spaces(df)

    print("Step 3/4: Handling null values...")
    df = handle_nulls(df, strategy)

    print("Step 4/4: Converting data types...")
    df = data_type_conversion(df, dataType_list)

    print("\n[OK] Dataset transformed successfully:")
    print(df.head())
    print(f"\n[INFO] Final shape: {df.shape}")
    print(f"[INFO] Final records: {len(df):,}")

    df.to_csv(
        "./data/processed/hotel_booking_clean.csv",
        index=False,
    )
    print(
        "[OK] Clean data saved to: "
        "./data/processed/hotel_booking_clean.csv"
    )

    return df


def create_normalized_dimension(
    df: pd.DataFrame,
    columns: list[str],
    id_name: str,
):
    """Create a normalized dimension with a sequential surrogate key."""
    dimension = df[columns].drop_duplicates().reset_index(drop=True)
    dimension.insert(0, id_name, range(1, len(dimension) + 1))
    return dimension


def create_dimensions(df: pd.DataFrame):
    """Create all dimensions from the transformed DataFrame."""
    print("\n[DIMENSIONS] Creating normalized dimensions...")

    return {
        "dim_dates": create_normalized_dimension(
            df,
            [
                "arrival_date_year",
                "arrival_date_month",
                "arrival_date_week_number",
                "arrival_date_day_of_month",
            ],
            "date_id",
        ),
        "dim_customers": create_normalized_dimension(
            df,
            [
                "adults",
                "children",
                "babies",
                "country",
                "customer_type",
                "is_repeated_guest",
            ],
            "customer_id",
        ),
        "dim_rooms": create_normalized_dimension(
            df,
            ["reserved_room_type", "assigned_room_type"],
            "room_id",
        ),
        "dim_sales": create_normalized_dimension(
            df,
            ["adr"],
            "sales_id",
        ),
        "dim_marketing": create_normalized_dimension(
            df,
            ["market_segment", "distribution_channel"],
            "marketing_id",
        ),
        "dim_history": create_normalized_dimension(
            df,
            [
                "previous_cancellations",
                "previous_bookings_not_canceled",
            ],
            "history_id",
        ),
        "dim_services": create_normalized_dimension(
            df,
            [
                "meal",
                "required_car_parking_spaces",
                "total_of_special_requests",
            ],
            "service_id",
        ),
        "dim_agent": create_normalized_dimension(
            df,
            ["agent", "company"],
            "agent_id",
        ),
        "dim_guest_stays": create_normalized_dimension(
            df,
            [
                "stays_in_weekend_nights",
                "stays_in_week_nights",
                "days_in_waiting_list",
            ],
            "stay_id",
        ),
    }


def create_fact_table(df: pd.DataFrame, dims: dict[str, pd.DataFrame]):
    """Create the fact table and add the dimension foreign keys."""
    print("\n[FACT] Creating fact_reservations...")

    # Keep all columns required for the dimension joins while the fact
    # table is being built. They are removed at the end.
    fact = df.copy()
    fact.insert(0, "reservation_id", range(1, len(fact) + 1))

    joins = [
        (
            "dim_dates",
            [
                "arrival_date_year",
                "arrival_date_month",
                "arrival_date_week_number",
                "arrival_date_day_of_month",
            ],
            "date_id",
            "fk_date_id",
        ),
        (
            "dim_customers",
            [
                "adults",
                "children",
                "babies",
                "country",
                "customer_type",
                "is_repeated_guest",
            ],
            "customer_id",
            "fk_customer_id",
        ),
        (
            "dim_rooms",
            ["reserved_room_type", "assigned_room_type"],
            "room_id",
            "fk_room_id",
        ),
        (
            "dim_sales",
            ["adr"],
            "sales_id",
            "fk_sales_id",
        ),
        (
            "dim_marketing",
            ["market_segment", "distribution_channel"],
            "marketing_id",
            "fk_marketing_id",
        ),
        (
            "dim_history",
            [
                "previous_cancellations",
                "previous_bookings_not_canceled",
            ],
            "history_id",
            "fk_history_id",
        ),
        (
            "dim_services",
            [
                "meal",
                "required_car_parking_spaces",
                "total_of_special_requests",
            ],
            "service_id",
            "fk_service_id",
        ),
        (
            "dim_agent",
            ["agent", "company"],
            "agent_id",
            "fk_agent_id",
        ),
        (
            "dim_guest_stays",
            [
                "stays_in_weekend_nights",
                "stays_in_week_nights",
                "days_in_waiting_list",
            ],
            "stay_id",
            "fk_stay_id",
        ),
    ]

    for dim_name, join_columns, id_column, fk_column in joins:
        fact = fact.merge(
            dims[dim_name],
            on=join_columns,
            how="left",
        ).rename(columns={id_column: fk_column})

    fact_columns = [
        "reservation_id",
        "hotel",
        "is_canceled",
        "lead_time",
        "booking_changes",
        "deposit_type",
        "reservation_status",
        "fk_date_id",
        "fk_customer_id",
        "fk_room_id",
        "fk_sales_id",
        "fk_marketing_id",
        "fk_history_id",
        "fk_service_id",
        "fk_agent_id",
        "fk_stay_id",
    ]

    return fact[fact_columns]


def run_etl(df: pd.DataFrame):
    """
    Run the complete transformation part of the ETL.

    The input is the DataFrame returned by extract.get_data().
    This function reuses transform_data() and then creates the
    dimensions and fact table. It does not load anything into PostgreSQL.
    """
    print("\n" + "=" * 70)
    print("TRANSFORM ETL")
    print("=" * 70)

    df = transform_data(df)
    dims = create_dimensions(df)
    fact = create_fact_table(df, dims)

    tables = {
        **dims,
        "fact_reservations": fact,
    }

    print("\n[OK] Transformation, dimensions and fact table completed")
    return tables