from extract import get_data

df = get_data('./data/raw/hotel_bookings.csv')



for col in df.columns:
    print(col)