from DbConnector import DbConnector
from tabulate import tabulate

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    # idle time = start of a trip minus the end of the previous trip of the same taxi
    # there is no end_time column so the end is start_time + duration in secs (same as task 8)
    # the subquery uses LAG to put the end of the previous trip (prev_end) next to each trip,
    # trips are ordered by start_time inside each taxi (PARTITION BY taxi_id)
    # the first trip of each taxi has no previous trip, its prev_end is NULL and AVG ignores it
    # some trips overlap in the data (next trip starts before the previous one ends),
    # GREATEST turns those negative gaps into 0 so they do not lower the average

    query = """
        SELECT
            taxi_id,
            COUNT(*) as total_trips,
            AVG(GREATEST(0, TIMESTAMPDIFF(SECOND, prev_end, start_time))) as avg_idle_seconds
        FROM (
            SELECT
                taxi_id,
                start_time,
                LAG(start_time + INTERVAL duration_seconds SECOND)
                    OVER (PARTITION BY taxi_id ORDER BY start_time, trip_id) as prev_end
            FROM trip
        ) g
        GROUP BY taxi_id
        ORDER BY avg_idle_seconds DESC
        LIMIT 20;
    """

    # the window function needs a temporary table for all the trips, with the default 16MB limit
    # it goes to /tmp on the server and fails with "The table is full", so we keep it in memory (256MB)
    cursor.execute("SET SESSION tmp_table_size = 268435456;")
    cursor.execute("SET SESSION max_heap_table_size = 268435456;")

    cursor.execute(query)
    top_taxis = cursor.fetchall()

    table_data = []
    place = 1
    for row in top_taxis:
        taxi_id = row[0]
        total_trips = row[1]
        avg_idle_seconds = row[2]

        table_data.append([
            place,
            taxi_id,
            total_trips,
            f"{avg_idle_seconds / 60:.1f} min",
            f"{avg_idle_seconds / 3600:.2f} h"
        ])
        place += 1

    headers = ["Place", "Taxi Number", "Trips", "Avg Idle (min)", "Avg Idle (h)"]

    print("\n=== Exercise 10 ===")
    print("Top 20 taxis with the highest average idle time between consecutive trips:")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()
