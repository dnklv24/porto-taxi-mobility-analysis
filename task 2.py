from DbConnector import DbConnector

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    # take trips per taxi
    query = """
        SELECT COUNT(trip_id) / COUNT(DISTINCT taxi_id) 
        FROM trip;
    """
    cursor.execute(query)
    
    # extract value from the result
    average_trips = cursor.fetchone()[0]

    print("\n=== Exercise 2 ===")
    print(f"On average each car completed: {average_trips:.0f}")
    print("=========================")

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()
