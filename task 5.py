from DbConnector import DbConnector
from tabulate import tabulate

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    print("Calculating top 20 taxis using Haversine formula and optimized query...")
    
    # subbquery quickly finds the top 20 taxis by total hours
    # haversine formula calculates the exact distance only for those 20 taxis
    query = """
        SELECT 
            t.taxi_id,
            top_taxis.total_hours,
            SUM(
                6371 * 2 * ASIN(SQRT(
                    POWER(SIN(RADIANS(t.end_lat - t.start_lat) / 2), 2) +
                    COS(RADIANS(t.start_lat)) * COS(RADIANS(t.end_lat)) *
                    POWER(SIN(RADIANS(t.end_lon - t.start_lon) / 2), 2)
                ))
            ) as total_distance_km
        FROM trip t
        JOIN (
            SELECT taxi_id, SUM(duration_seconds) / 3600 as total_hours
            FROM trip
            GROUP BY taxi_id
            ORDER BY total_hours DESC
            LIMIT 20
        ) top_taxis ON t.taxi_id = top_taxis.taxi_id
        WHERE t.start_lat IS NOT NULL AND t.end_lat IS NOT NULL
        GROUP BY t.taxi_id, top_taxis.total_hours
        ORDER BY top_taxis.total_hours DESC;
    """
    cursor.execute(query)
    top_taxis = cursor.fetchall()

    table_data = []
    place = 1
    for row in top_taxis:
        taxi_id = row[0]
        total_hours = row[1]
        total_distance = row[2]
        
        table_data.append([
            place,
            taxi_id,
            f"{total_hours:.1f} h",
            f"{total_distance:.1f} km"
        ])
        place += 1

    headers = ["Place", "Taxi Number", "Total Hours", "Total Distance"]

    print("\n=== Exercise 5  ===")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()
