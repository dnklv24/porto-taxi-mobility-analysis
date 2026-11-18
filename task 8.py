from DbConnector import DbConnector
from tabulate import tabulate

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    # there is no variable end_time so we add duration in secs to start_time
    # if the date part of start_time is different from the date part of our end_time, 
    # it means the trip crossed midnight
    
    query = """
        SELECT 
            trip_id, 
            start_time, 
            start_time + INTERVAL duration_seconds SECOND as end_time
        FROM trip
        WHERE DATE(start_time) != DATE(start_time + INTERVAL duration_seconds SECOND);
    """
    cursor.execute(query)
    trips = cursor.fetchall()

    print("\n=== Exercise 8 ===")
    print(f"Total trips crossing midnight: {len(trips)}")
    
    # we prepare table data for the first 20 trips to avoid hanging
    table_data = []
    for i in range(min(20, len(trips))):
        trip_id = trips[i][0]
        start = trips[i][1]
        end = trips[i][2]
        table_data.append([i + 1, trip_id, start, end])

    headers = ["#", "Trip ID", "Start Time", "End Time"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
            
    if len(trips) > 20:
        print("... etc.")

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()
