# Python Training Course
# Student: Semeniuk Pavlo
## Task on branch `main`: Weather getter for specific city and date
## Task on branch `practice`: 22 practice tasks


## How to use it:

``
pip install openmeteo-requests geopy pandas pytz
``

Usage
-----

To use the application, follow the steps below:

1. Enter the name of the city for which you want to retrieve the weather forecast.
2. Enter the start date of the forecast in the format `DD-MM-YYYY`.
3. Enter the end date of the forecast in the format `DD-MM-YYYY`. The end date must be later than or equal to the start date and be within 7 days after the start date.
4. The application will retrieve the hourly weather forecast for the specified city and date range and display it in a table.

The table will contain the following columns:

* `Hour`: The hour of the day in the format `HH:MM`.
* `Day`: The date of the forecast in the format `YYYY-MM-DD`.
* `Temperature`: The temperature in degrees Celsius.
* `Rain Prob`: The probability of rain in percent.
* `Weather`: A description of the weather conditions.

Note
-----

Temperature, Rain Prob and Weather columns are combined into one for a specific hour of the day in such order