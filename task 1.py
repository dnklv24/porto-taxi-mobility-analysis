from DbConnector import DbConnector

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    # use cursor to count taxis
    cursor.execute("SELECT COUNT(*) FROM taxi;")
    # fetchone() takes cursor out of BD, [0] takes the number itself
    taxi_count = cursor.fetchone()[0]

    # use cursor to count trips
    cursor.execute("SELECT COUNT(*) FROM trip;")
    trip_count = cursor.fetchone()[0]

    # use cursor to count points
    cursor.execute("SELECT COUNT(*) FROM trip_point;")
    point_count = cursor.fetchone()[0]

    # answer display
    print("\n   Exercise 1   ")
    print(f"Total taxis: {taxi_count}")
    print(f"Total trips: {trip_count}")
    print(f"Total GPS points: {point_count}")
    print("=========================")

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()
