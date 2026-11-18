from DbConnector import DbConnector

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    # count trips per taxi and take 20 positions of ordered list
    query = """
        SELECT taxi_id, COUNT(trip_id) as total_trips
        FROM trip
        GROUP BY taxi_id
        ORDER BY total_trips DESC
        LIMIT 20;
    """
    cursor.execute(query)
    
    # take all 20 rows from the result
    top_taxis = cursor.fetchall()

    print("\n=== Exercise 3 ===")
    print("Top-2o taxis with the biggest number of trips:")
    print("Place | Taxi number | Trips completed")
    print("-" * 33)
    
    # print info for each taxi
    place = 1
    for row in top_taxis:
        taxi_id = row[0]
        trips = row[1]
        print(f"{place:2d}.   | {taxi_id:<11} | {trips}")
        place += 1
        
    print("=========================")

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()

