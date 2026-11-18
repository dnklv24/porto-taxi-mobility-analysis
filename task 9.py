from DbConnector import DbConnector
from tabulate import tabulate

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    # start and end coordinates are already stored in the 'trip' table
    # the subquery computes the distance in meters between the start and the end of each trip
    # (ST_Distance_Sphere, POINT takes longitude first), the outer query keeps the ones within 50m
    # we need the subquery because dist_m can not be used in the WHERE of the same SELECT

    query = """
        SELECT trip_id, taxi_id, start_time, num_points, dist_m
        FROM (
            SELECT
                trip_id, taxi_id, start_time, num_points,
                ST_Distance_Sphere(POINT(start_lon, start_lat), POINT(end_lon, end_lat)) AS dist_m
            FROM trip
        ) sub
        WHERE dist_m <= 50;
    """
    cursor.execute(query)
    trips = cursor.fetchall()

    print("\n=== Exercise 9 ===")
    print(f"Total circular trips (start and end within 50m): {len(trips)}")

    # we prepare table data for the first 20 trips to avoid hanging
    table_data = []
    for i in range(min(20, len(trips))):
        trip_id, taxi_id, start, num_points, dist_m = trips[i]
        table_data.append([i + 1, trip_id, taxi_id, start, num_points, f"{dist_m:.1f} m"])

    headers = ["#", "Trip ID", "Taxi Number", "Start Time", "GPS Points", "Start-End Distance"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    if len(trips) > 20:
        print("... etc.")

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()
