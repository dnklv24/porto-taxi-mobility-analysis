from DbConnector import DbConnector
from tabulate import tabulate

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor
    
    # for each call type count the trips, average duration and distance in kms by time band
    # using Haversine formula for accurate distance calculation
    query = """
        SELECT 
            call_type,
            COUNT(trip_id) as total_trips,
            AVG(duration_seconds) as avg_duration_sec,
            SUM(CASE WHEN HOUR(start_time) >= 0 AND HOUR(start_time) < 6 THEN 1 ELSE 0 END) as h0_6,
            SUM(CASE WHEN HOUR(start_time) >= 6 AND HOUR(start_time) < 12 THEN 1 ELSE 0 END) as h6_12,
            SUM(CASE WHEN HOUR(start_time) >= 12 AND HOUR(start_time) < 18 THEN 1 ELSE 0 END) as h12_18,
            SUM(CASE WHEN HOUR(start_time) >= 18 AND HOUR(start_time) < 24 THEN 1 ELSE 0 END) as h18_24,
            AVG(
                6371 * 2 * ASIN(SQRT(
                    POWER(SIN(RADIANS(end_lat - start_lat) / 2), 2) +
                    COS(RADIANS(start_lat)) * COS(RADIANS(end_lat)) *
                    POWER(SIN(RADIANS(end_lon - start_lon) / 2), 2)
                ))
            ) as avg_distance_km 
            
        FROM trip
        WHERE start_lat IS NOT NULL AND end_lat IS NOT NULL
        GROUP BY call_type;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    table_data = []
    for row in results:
        call_type = row[0]
        total_trips = row[1]
        avg_duration_sec = row[2]
        
        # turn seconds into minutes
        avg_duration_minutes = avg_duration_sec / 60
        
        # count shares (percentages)
        share_0_6 = (row[3] / total_trips) * 100
        share_6_12 = (row[4] / total_trips) * 100
        share_12_18 = (row[5] / total_trips) * 100
        share_18_24 = (row[6] / total_trips) * 100
        
        # get average distance calculated with Haversine
        avg_distance_km = row[7]
        
        table_data.append([
            call_type,
            f"{avg_duration_minutes:.1f} min",
            f"{avg_distance_km:.1f} km",
            f"{share_0_6:.1f}%",
            f"{share_6_12:.1f}%",
            f"{share_12_18:.1f}%",
            f"{share_18_24:.1f}%"
        ])

    headers = ["Type", "Avg Duration", "Avg Distance", "00-06", "06-12", "12-18", "18-24"]

    print("\n=== Exercise 4b ===")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()
