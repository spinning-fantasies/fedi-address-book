import json
from datetime import datetime
from icalendar import Calendar, Event

# Read the JSON file
json_filename = 'followers.json'  # Replace with your JSON file's name
with open(json_filename, 'r') as json_file:
    data = json.load(json_file)

# Create a new iCalendar
cal = Calendar()

# Iterate through the JSON data and create anniversary events
for item in data:
    event = Event()
    # event.add('summary', item.get('display_name', 'Unnamed Anniversary'))
    event.add('summary', f'Fediversary: {item["display_name"]}')
    
    # Parse date string from JSON and convert to datetime object
    anniversary_date = datetime.strptime(item['created_at'], '%Y-%m-%d')
    event.add('dtstart', anniversary_date)
    event.add('rrule', {'freq': 'yearly'})  # Set recurrence rule to yearly
    
    cal.add_component(event)

# Save the iCalendar to a file
ics_filename = 'fediversaries.ics'  # Replace with your desired output file name
with open(ics_filename, 'wb') as ics_file:
    ics_file.write(cal.to_ical())

print(f'Generated {ics_filename} successfully!')
