from src.GoogleTools.CalendarTools import get_calendar_events

events = get_calendar_events(calendar_id='vog4t60q4i2u35ol717387am5g@group.calendar.google.com',
                             start_date='2022-01-01', end_date='2023-01-31', search_string='SCL')
print(events)
