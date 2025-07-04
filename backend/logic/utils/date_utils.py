from datetime import datetime, timedelta, timezone

def format_date(timestamp, subtract_seconds=0):
        dt_object = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        dt_object = dt_object - timedelta(seconds=subtract_seconds)
        formatted_date = dt_object.isoformat(timespec='milliseconds')
        return formatted_date
