# REQUIRED USER CONFIGURATION

Replace every empty value before turning on `LIVE` submission.
Do not set `RUN_MODE` in this file. The only mode switch is `config/runtime.md`, which defaults to `RUN_MODE=REVIEW_ONLY`.

## Locations

TARGET_LOCATIONS=Vadodara; Ahmedabad; Mumbai; Pune; Bangalore; Dubai, UAE; Seoul, South Korea; New York, USA; Toronto, Canada; Vancouver, Canada; London, UK; Paris, France; Sydney, Australia; other suitable locations across Europe
ACCEPT_REMOTE=YES
ACCEPT_HYBRID=YES
ACCEPT_ONSITE=YES
OPEN_TO_RELOCATION=YES
OPEN_TO_INTERNATIONAL_RELOCATION=YES
ACCEPTED_COUNTRIES=India; United Arab Emirates; South Korea; United States; Canada; United Kingdom; France; Australia; other suitable European countries
ACCEPTED_CITIES=Vadodara; Ahmedabad; Mumbai; Pune; Bangalore; Dubai; Seoul; New York; Toronto; Vancouver; London; Paris; Sydney

## Compensation

MIN_MONTHLY_SALARY_INR=20000
PREFERRED_MONTHLY_SALARY_INR=MARKET_RANGE_FOR_ROLE_AND_LOCATION
INTERNATIONAL_SALARY_RULE=MARKET_RANGE_FOR_ROLE_AND_LOCATION

## Schedule / workplace

PREFERRED_SHIFTS=Day
MAX_WORKDAYS_PER_WEEK=5
ACCEPT_NIGHT_SHIFTS=YES_ONLY_IF_FULLY_REMOTE
ACCEPT_ROTATIONAL_SHIFTS=YES_ONLY_IF_FULLY_REMOTE
AVAILABILITY=Immediately

## Application answers

AVAILABILITY=Immediately
WORK_AUTHORIZATION_INDIA=Yes, I am authorized to work in India.
WORK_AUTHORIZATION_INTERNATIONAL=I do not currently hold international work authorization. I am open to relocation and would require employer-sponsored work authorization where sponsorship is required.
VISA_SPONSORSHIP=I would require employer sponsorship in countries where employer-sponsored work authorization is required.
RELOCATION_ANSWER=Yes, I’m open to relocating for the right opportunity, including international relocation. I’m particularly interested in opportunities where relocation support or employer-sponsored work authorization is available when required.
SALARY_EXPECTATION_INDIA=I’m open to discussing compensation based on the role, responsibilities, location, and prevailing market range. For India-based opportunities, I’m targeting roles starting around ₹20,000 per month, with flexibility for the right opportunity.
SALARY_EXPECTATION_INTERNATIONAL=I’m open to discussing compensation based on the role, location, responsibilities, and prevailing market range for the position. I’m flexible for the right opportunity and would be happy to discuss the employer’s budgeted range.

## Tracker

SPREADSHEET_ID=NOT_CONFIGURED

The spreadsheet name to create or connect is `Job Applications — Master Tracker`.
The automation reads `SPREADSHEET_ID` from `config/runtime.md`.
Paste the real Google Sheet ID in `config/runtime.md` on the `SPREADSHEET_ID=` line, replacing `NOT_CONFIGURED`, and set the same value on the `SPREADSHEET_ID=` line in this file.
Do not invent an ID.

## Outreach

RECRUITER_OUTREACH_ENABLED=NO
