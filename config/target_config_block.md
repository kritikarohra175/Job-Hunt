# REQUIRED USER CONFIGURATION

Approved values are recorded here and in the canonical files they mirror.
Do not set `RUN_MODE` in this file. The only mode switch is `config/runtime.md`, which is `RUN_MODE=REVIEW_ONLY`.

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

India monthly INR rules: an entire stated range below ₹20,000/month is a rejection. A range that overlaps ₹20,000/month is review. A range that starts at or above ₹20,000/month is eligible only when every other criterion passes. Do not invent a salary or convert another currency into INR.

## Schedule / workplace

PREFERRED_SHIFTS=Day
MAX_WORKDAYS_PER_WEEK=5
ACCEPT_NIGHT_SHIFTS=YES_ONLY_IF_FULLY_REMOTE
ACCEPT_ROTATIONAL_SHIFTS=YES_ONLY_IF_FULLY_REMOTE
AVAILABILITY=Immediately

## Application answers

Use the exact wording in `config/answer_bank.md`.

WORK_AUTHORIZATION_INDIA=Yes, I am authorized to work in India.
WORK_AUTHORIZATION_INTERNATIONAL=I do not currently hold international work authorization. I am open to relocation and would require employer-sponsored work authorization where sponsorship is required.
VISA_SPONSORSHIP=I would require employer sponsorship in countries where employer-sponsored work authorization is required.
RELOCATION_ANSWER=Yes, I’m open to relocating for the right opportunity, including international relocation. I’m particularly interested in opportunities where relocation support or employer-sponsored work authorization is available when required.
SALARY_EXPECTATION_INDIA=I’m open to discussing compensation based on the role, responsibilities, location, and prevailing market range. For India-based opportunities, I’m targeting roles starting around ₹20,000 per month, with flexibility for the right opportunity.
SALARY_EXPECTATION_INTERNATIONAL=I’m open to discussing compensation based on the role, location, responsibilities, and prevailing market range for the position. I’m flexible for the right opportunity and would be happy to discuss the employer’s budgeted range.

## Tracker

SPREADSHEET_ID=1M-cW2cUDfcUAQTGU5T9pNMs_rW_pXZhvhq-kjasD6JI
SPREADSHEET_NAME=Job Applications — Master Tracker
TRACKER_TAB=Applications

The automation reads `SPREADSHEET_ID` from `config/runtime.md`. This file must match that value. Do not invent an ID.

## Drive

DRIVE_MASTER_RESUME_FILE_ID=1xjtepznMiLTdQnWGMIujIlWww15PY5UX
DRIVE_MASTER_RESUME_FOLDER_ID=1cfBsRht8TOJ7e5PsBcIRlnoQrUdUaOG8
DRIVE_TAILORED_RESUMES_FOLDER_ID=1uoZnYXfHaCa8jRC9aEQ3BLq3NFFwq_Fo

The Drive master file is a byte-identical copy of `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`. It is the only Drive resume that may be used.

## Outreach

RECRUITER_OUTREACH_ENABLED=NO
