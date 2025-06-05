@app.get("/events/upcoming/", response_model=List[EventCreate])
def list_upcoming_events():
    db = SessionLocal()
    events = db.query(Event).filter(Event.event_date > date.today()).all()
    db.close()
    return events
def list_upcoming_events():
    print("\n--- List Upcoming Events ---")
    try:
        response = requests.get(f"{API_URL}/events/upcoming/")
        if response.status_code == 200:
            events = response.json()
            for event in events:
                print(json.dumps(event, indent=4))
        else:
            print("Error:", response.json())
    except Exception as e:
        print("An error occurred while listing upcoming events:", str(e))
