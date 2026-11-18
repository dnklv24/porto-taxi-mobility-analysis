from DbConnector import DbConnector

def main():
    # open DB
    db = DbConnector()
    cursor = db.cursor

    # get the numbers for all taxis and sort them from biggest to smallest
    query = """
        SELECT taxi_id, call_type, COUNT(trip_id) as total_calls
        FROM trip
        GROUP BY taxi_id, call_type
        ORDER BY taxi_id, total_calls DESC;
    """
    cursor.execute(query)
    
    # take all rows from the result
    all_counts = cursor.fetchall()

    print("\n=== Exercise 4a ===")
    print("Most used call type per taxi:")
    print("Taxi number | Call type | Trips completed")
    print("-" * 43)
    
    # mark the taxis that have already been analyzed
    viewed_taxis = set()
    printed_count = 0
    
    for row in all_counts:
        taxi_id = row[0]
        call_type = row[1]
        total_calls = row[2]
        
        # if taxi number appear for the 1st time then we see its biggest call type
        if taxi_id not in viewed_taxis:
            print(f"{taxi_id:<11} | {call_type:<9} | {total_calls}")
            viewed_taxis.add(taxi_id) # adding taxi  to already analyzed ones
            printed_count += 1
            
            
    print("=========================")

    # close DB
    db.close_connection()

if __name__ == '__main__':
    main()