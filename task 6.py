from DbConnector import DbConnector

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    # we use Bounding Box optimization:
    # we draw a rough square (bounding box) of  approximatelt 100x100m around the City Hall
    # latitude +/- 0.0009 degrees is approx 100m.
    # longitude +/- 0.0012 degrees is approx 100m at this latitude.
    # we filter points inside this square first
    # then we apply the Pythagorean formula solely to the points inside the square 
    # to get an exact 100m circle (<= 0.1 km) 
    
    query = """
        SELECT DISTINCT trip_id
        FROM trip_point
        WHERE 
            latitude BETWEEN (41.15794 - 0.0009) AND (41.15794 + 0.0009)
            AND longitude BETWEEN (-8.62911 - 0.0012) AND (-8.62911 + 0.0012)
            
            AND 111 * SQRT(POWER(latitude - 41.15794, 2) + POWER(longitude - (-8.62911), 2)) <= 0.1;
    """
    cursor.execute(query)
    trips = cursor.fetchall()

    print("\n=== Exercise 6 ===")
    print(f"Total trips that passed within 100m of City Hall: {len(trips)}")
    print("-" * 50)
    
    # only print first 20 trips to avoid hanging
    print("Example trip IDs:")
    for i in range(min(20, len(trips))):
        print(f"- {trips[i][0]}")
            
    if len(trips) > 20:
        print("... etc.")
    print("================================================")

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()