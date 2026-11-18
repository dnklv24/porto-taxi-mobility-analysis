from DbConnector import DbConnector

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor
    
    # instead of doing a GROUP BY on the 82M row 'trip_point' table, 
    # we just use the pre-calculated 'num_points' column in the 'trip' table
    
    query = """
        SELECT COUNT(trip_id)
        FROM trip
        WHERE num_points < 3;
    """
    cursor.execute(query)
    
    # extract one number which is the total number of invalid trips
    result = cursor.fetchone()
    invalid_trips_count = result[0]

    print("\n=== Exercise 7  ===")
    print(f"Number of invalid trips (< 3 GPS points): {invalid_trips_count}")
    print("==================================")

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()