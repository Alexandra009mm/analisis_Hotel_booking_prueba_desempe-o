import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()


def create_connection():
    """Create the PostgreSQL SQLAlchemy connection from environment variables."""
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5433")
    database = os.getenv("PGDATABASE")

    if not user or not password or not database:
        raise ValueError(
            "Required environment variables: "
            "PGUSER, PGPASSWORD, PGDATABASE"
        )

    url = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{host}:{port}/{database}"
    )
    return create_engine(url)


def load_to_postgres(
    df,
    table_name: str,
    if_exists: str = "replace",
):
    """Load one DataFrame into PostgreSQL."""
    engine = create_connection()

    try:
        print(f"[LOAD] Loading table: {table_name} ({len(df):,} rows)")

        df.to_sql(
            table_name,
            con=engine,
            if_exists=if_exists,
            index=False,
            method="multi",
        )

        with engine.connect() as conn:
            result = conn.execute(
                text(f'SELECT COUNT(*) FROM "{table_name}"')
            )
            total = result.scalar()

        print(f"[OK] {total:,} records in {table_name}")

    except Exception as e:
        print(f"[ERROR] Loading {table_name}: {e}")
        raise
    finally:
        engine.dispose()


def create_primary_keys():
    """Create primary keys after the tables have been loaded."""
    engine = create_connection()

    primary_keys = [
        ("dim_dates", "date_id"),
        ("dim_customers", "customer_id"),
        ("dim_rooms", "room_id"),
        ("dim_sales", "sales_id"),
        ("dim_marketing", "marketing_id"),
        ("dim_history", "history_id"),
        ("dim_services", "service_id"),
        ("dim_agent", "agent_id"),
        ("dim_guest_stays", "stay_id"),
        ("fact_reservations", "reservation_id"),
    ]

    try:
        with engine.begin() as conn:
            for table, column in primary_keys:
                exists = conn.execute(
                    text(
                        """
                        SELECT 1
                        FROM information_schema.table_constraints
                        WHERE constraint_schema = 'public'
                          AND table_name = :table
                          AND constraint_name = :constraint
                        """
                    ),
                    {
                        "table": table,
                        "constraint": f"pk_{table}",
                    },
                ).fetchone()

                if not exists:
                    conn.execute(
                        text(
                            f'ALTER TABLE "{table}" '
                            f'ADD CONSTRAINT "pk_{table}" '
                            f'PRIMARY KEY ("{column}")'
                        )
                    )
                    print(f"[OK] PK created: {table}.{column}")
    finally:
        engine.dispose()


def create_foreign_keys():
    """Create all fact-to-dimension relationships."""
    create_primary_keys()
    engine = create_connection()

    foreign_keys = [
        (
            "fk_fact_dates",
            "fact_reservations",
            "fk_date_id",
            "dim_dates",
            "date_id",
        ),
        (
            "fk_fact_customers",
            "fact_reservations",
            "fk_customer_id",
            "dim_customers",
            "customer_id",
        ),
        (
            "fk_fact_rooms",
            "fact_reservations",
            "fk_room_id",
            "dim_rooms",
            "room_id",
        ),
        (
            "fk_fact_sales",
            "fact_reservations",
            "fk_sales_id",
            "dim_sales",
            "sales_id",
        ),
        (
            "fk_fact_marketing",
            "fact_reservations",
            "fk_marketing_id",
            "dim_marketing",
            "marketing_id",
        ),
        (
            "fk_fact_history",
            "fact_reservations",
            "fk_history_id",
            "dim_history",
            "history_id",
        ),
        (
            "fk_fact_services",
            "fact_reservations",
            "fk_service_id",
            "dim_services",
            "service_id",
        ),
        (
            "fk_fact_agents",
            "fact_reservations",
            "fk_agent_id",
            "dim_agent",
            "agent_id",
        ),
        (
            "fk_fact_stays",
            "fact_reservations",
            "fk_stay_id",
            "dim_guest_stays",
            "stay_id",
        ),
    ]

    try:
        with engine.begin() as conn:
            for constraint, source_table, source_column, target_table, target_column in foreign_keys:
                exists = conn.execute(
                    text(
                        """
                        SELECT 1
                        FROM information_schema.table_constraints
                        WHERE constraint_schema = 'public'
                          AND constraint_name = :constraint
                        """
                    ),
                    {"constraint": constraint},
                ).fetchone()

                if not exists:
                    conn.execute(
                        text(
                            f'ALTER TABLE "{source_table}" '
                            f'ADD CONSTRAINT "{constraint}" '
                            f'FOREIGN KEY ("{source_column}") '
                            f'REFERENCES "{target_table}" ("{target_column}")'
                        )
                    )
                    print(
                        f"[OK] FK: {source_table}.{source_column} "
                        f"-> {target_table}.{target_column}"
                    )
    finally:
        engine.dispose()