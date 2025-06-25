from datetime import datetime
import pytz
from fastapi import HTTPException

def convert_timezone(dt_str: str, from_tz: str, to_tz: str) -> str:
    try:
        dt_naive = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")

        from_timezone = pytz.timezone(from_tz)
        dt_localized = from_timezone.localize(dt_naive)

        to_timezone = pytz.timezone(to_tz)
        dt_converted = dt_localized.astimezone(to_timezone)

        return dt_converted.isoformat()

    except pytz.UnknownTimeZoneError:
        raise HTTPException (
            status_code=400, 
            detail=f"Invalid timezone: '{to_tz}'. Please use a valid timezone (America/New_York, Europe/London, etc)."
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error converting time: {str(e)}"
        )
