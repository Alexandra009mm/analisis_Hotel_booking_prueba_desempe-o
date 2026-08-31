import pandas as pd


# --------------------------------------------------------------------------
#  function that normalizes text columns
# --------------------------------------------------------------------------


def column_normalization(
    df: pd.DataFrame,
):  # Verify the parameter's data type is dataframe.
    """
    Normalize the names of each column.

    TRANSFORMS:
        1. Remove spaces at the beginning and end
        2. Convert to lowercase
        3. Replace spaces with underscores
        4. Remove accents and ñ

    EXAMPLE:
        BEFORE: [" Customer Code ", "sales Date", "import Total Ñoño"]
        AFTER: ["customer_code", "sales_date", "import_total_nono"]
    """

    df = df.copy()

    df.columns = (
        df.columns.str.strip()  # Remove spaces
        .str.lower()  # Convert to lowercase
        .str.replace(" ", "_", regex=False)  # Replace spaces
        .str.replace("á", "a", regex=False)  # Remove accents
        .str.replace("é", "e", regex=False)
        .str.replace("í", "i", regex=False)
        .str.replace("ó", "o", regex=False)
        .str.replace("ú", "u", regex=False)
        .str.replace("ñ", "n", regex=False)
    )

    print("[TRANSFORM] Columns normalized")

    return df


# --------------------------------------------------------------------------
#  function that clean up spaces in text
# --------------------------------------------------------------------------


def clean_text_spaces(
    df: pd.DataFrame,
):  # Verify the parameter's data type is dataframe.
    """
    Clean extra spaces from text columns.

    PROCESS:
        1. Identify columns of type 'object' or 'string'
        2. Convert values to string
        3. Remove spaces at the beginning and end

    EXAMPLE:
        BEFORE: '  Hotel Libertad  '
        AFTER: 'Hotel Libertad'
    """

    df = df.copy()

    text_columns = df.select_dtypes(include=["object", "string"]).columns

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    print(f"[TRANSFORM] Spaces cleaned in {len(text_columns)} text columns")

    return df


# --------------------------------------------------------------------------
#  function that change the data type of each column
# --------------------------------------------------------------------------


def data_type_conversion(
    df: pd.DataFrame, types: dict[str, str]
):  # Verify the parameter's data type is dataframe and diccionary.
    """
    Convert DataFrame columns to the specified data types.

    PARAMETERS:
        df (pd.DataFrame): DataFrame to transform.
        types (dict): Mapping of column names to data types.

    EXAMPLE:
        types = {
            'adults':'int64',
            'is_cancele: 'bool',
            'adr': 'float64'
        }

        df = data_type_conversion(df, types)
    """

    df = df.copy()

    for column, data_type in types.items():
        if column in df.columns:
            try:
                df[column] = df[column].astype(data_type)
            except Exception as e:
                print(
                    f"[WARNING] Could not convert "
                    f"{column} to {data_type}: {e}"
                )

    print("[TRANSFORM] Data types converted")

    return df


# --------------------------------------------------------------------------------------
# This function handles null values ​​and how to convert them according to my parameters.
# --------------------------------------------------------------------------------------


def handle_nulls(
    df: pd.DataFrame, strategy: dict = None
):  # Verify the parameter's data type is dataframe and a diccionary.
    """
    Handle null values in a DataFrame.

    PARAMETERS:
        df (pd.DataFrame): DataFrame to transform.
        strategy (dict): Mapping of column names to null-handling strategies.

    AVAILABLE STRATEGIES:
        - A value: Fill nulls with that value.
        - 'mean': Fill nulls with the column mean.
        - 'mode': Fill nulls with the column mode.
        - 'drop': Remove rows containing null values.

    NOTE:
        Columns not included in the strategy are left unchanged.

    EXAMPLE:
        strategy = {
            'children': 0,
            'adr': 'mean',
            'meal': 'mode',
            'agent': 'drop'
        }

        df = handle_nulls(df, strategy)
    """

    df = df.copy()

    if strategy is None:
        strategy = {}

    for column, method in strategy.items():

        if column not in df.columns:
            continue

        nulls = df[column].isnull().sum()

        if nulls == 0:
            continue

        if method == "drop":
            df = df.dropna(subset=[column])

        elif method == "mean":
            df[column] = df[column].fillna(df[column].mean())

        elif method == "mode":
            df[column] = df[column].fillna(df[column].mode()[0])

        else:
            df[column] = df[column].fillna(method)

    print("[TRANSFORM] Null values handled")

    return df


# ---------------------------------------------------------------------------------------------------------------
#  function removes duplicates from the DataFrame; ideal for use after normalizing communes and data types.
# ---------------------------------------------------------------------------------------------------------------
def remove_duplicates(
    df: pd.DataFrame, subset: list[str] = None
):  # Verify the parameter's data type is dataframe and a list.
    """
    Remove duplicate records from a DataFrame.

    PARAMETERS:
        df (pd.DataFrame):
            DataFrame to process.

        subset (List[str], optional):
            Columns used to identify duplicate records.
            If None, all columns are considered.

    RETURNS:
        pd.DataFrame:
            DataFrame without duplicate records.

    EXAMPLES:

        # Remove duplicate hotel reservations
             df = remove_duplicates(
                df,
                subset=['arrival_date', 'email', 'hotel']
             )

    NOTES:
        - Keeps the first occurrence of each duplicate.
        - Returns a copy of the original DataFrame.
        - Does not modify the original DataFrame.
    """

    df = df.copy()

    rows_before = len(df)

    df = df.drop_duplicates(subset=subset, keep="first")

    duplicates_removed = rows_before - len(df)

    if duplicates_removed > 0:
        print(
            f"[TRANSFORM] {duplicates_removed:,} "
            f"duplicate records removed"
        )
    else:
        print("[TRANSFORM] No duplicate records found")

    return df
