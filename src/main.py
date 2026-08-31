from extract import get_data
from transform import run_etl
from load import load_to_postgres, create_foreign_keys


def main():
    """Execute the complete Extract -> Transform -> Load pipeline."""
    print("=" * 70)
    print("HOTEL BOOKINGS ETL PIPELINE")
    print("=" * 70)

    # 1. EXTRACT
    print("\n[EXTRACT] Reading data...")
    df = get_data("./data/raw/hotel_bookings.csv")

    # 2. TRANSFORM + DIMENSIONS + FACT
    tables = run_etl(df)

    # 3. LOAD
    print("\n" + "=" * 70)
    print("LOADING DATA INTO POSTGRESQL")
    print("=" * 70)

    # Dimensions are loaded first so their primary keys exist before
    # the fact table relationships are created.
    dimension_order = [
        "dim_dates",
        "dim_customers",
        "dim_rooms",
        "dim_sales",
        "dim_marketing",
        "dim_history",
        "dim_services",
        "dim_agent",
        "dim_guest_stays",
    ]


    
    for table_name in dimension_order:
        load_to_postgres(
            tables[table_name],
            table_name,
            if_exists="replace",
        )

    load_to_postgres(
        tables["fact_reservations"],
        "fact_reservations",
        if_exists="replace",
    )

    # 4. RELATIONSHIPS
    print("\n" + "=" * 70)
    print("CREATING DATABASE RELATIONSHIPS")
    print("=" * 70)

    create_foreign_keys()

    print("\n" + "=" * 70)
    print("ETL PIPELINE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
