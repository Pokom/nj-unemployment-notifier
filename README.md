# Unemployment Notifier

Every week New Jersey Division of Unemployment posts a schedule of when you must submit
your claim. It's a 30 minute window that can change each week. You must go to the website
to see when your scheduled time is. It's very possible that your first time is Sunday at
8am and you would not know of it.

To solve this, I would like to write a program that will attempt to fetch the website and
find the timeslot for a specific social security number. Ideally this should generate
an alert.

## Problem

This can be broken down into four parts:

1. Download the NJ DOUE website
2. Parse the HTML and date and times for Social Security Ranges
3. Match an input Social Security number to the time
4. Generate an alert
