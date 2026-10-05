# Job Search Preferences

## Primary role family

Search for entry-level roles in:
- Digital Marketing
- Social Media Marketing
- Content Marketing
- SEO
- Marketing Operations / Marketing Associate
- Performance Marketing at true entry level
- Growth Marketing at true entry level
- Closely related digital marketing roles

## Strong title matches

Digital Marketing Executive
Digital Marketing Associate
Digital Marketing Coordinator
Digital Marketing Specialist – Entry Level
Digital Marketing Trainee
Social Media Executive
Social Media Associate
Social Media Coordinator
Social Media Marketing Executive
Social Media Marketing Associate
Content Marketing Executive
Content Marketing Associate
SEO Executive
SEO Associate
Marketing Executive
Marketing Associate
Digital Marketing Assistant
Growth Marketing Associate
Performance Marketing Executive – Entry Level
AI-assisted Marketing roles that are genuinely marketing roles

## Experience requirement

Preferred: 0 years / fresher / internship experience accepted.
Maximum automatic-apply threshold: 1 year.

If the JD states 1–2 years or equivalent but the role is clearly junior and the employer appears flexible, route to REVIEW instead of auto-submit.

Reject automatic application when the role clearly requires more than 2 years.

## Location

These location values are approved. Do not invent additional target cities.

TARGET_LOCATIONS=Vadodara; Ahmedabad; Mumbai; Pune; Bangalore; Dubai, UAE; Seoul, South Korea; New York, USA; Toronto, Canada; Vancouver, Canada; London, UK; Paris, France; Sydney, Australia; other suitable locations across Europe
ACCEPT_REMOTE=YES
ACCEPT_HYBRID=YES
ACCEPT_ONSITE=YES
OPEN_TO_RELOCATION=YES
OPEN_TO_INTERNATIONAL_RELOCATION=YES
ACCEPTED_COUNTRIES=India; United Arab Emirates; South Korea; United States; Canada; United Kingdom; France; Australia; other suitable European countries
ACCEPTED_CITIES=Vadodara; Ahmedabad; Mumbai; Pune; Bangalore; Dubai; Seoul; New York; Toronto; Vancouver; London; Paris; Sydney

India targets: Vadodara, Ahmedabad, Mumbai, Pune, Bangalore.
International targets: Dubai, UAE; Seoul, South Korea; New York, USA; Toronto, Canada; Vancouver, Canada; London, UK; Paris, France; Sydney, Australia.
Other suitable locations across Europe may be included when the role otherwise matches. Do not invent a city that is not named here and treat it as a required target.

Remote, hybrid, and on-site arrangements are all acceptable. The candidate is open to relocation, including international relocation.

## Salary

MIN_MONTHLY_SALARY_INR=20000
PREFERRED_MONTHLY_SALARY_INR=MARKET_RANGE_FOR_ROLE_AND_LOCATION
INTERNATIONAL_SALARY_RULE=MARKET_RANGE_FOR_ROLE_AND_LOCATION

The minimum acceptable salary for India-based roles is ₹20,000 per month.
Preferred salary, in India and internationally, is not a fixed number. Evaluate a disclosed range against the prevailing market range for the role and location.
Never invent or estimate a salary, a conversion, or a monthly equivalent.

### Salary filtering

Apply these rules only to a salary the posting actually states:

- Entire salary range below ₹20,000/month = Reject. This floor applies to India roles whose pay is stated in INR per month.
- Salary range overlaps ₹20,000/month = Review.
- Salary starts at or above ₹20,000/month = eligible if all other requirements pass.
- Never invent or estimate a salary.
- If salary is undisclosed, do not automatically reject solely because salary is unknown.

A range overlaps ₹20,000/month when it includes ₹20,000 or includes amounts both below and at or above ₹20,000. A stated monthly INR amount, or the start of a stated monthly INR range, that is ₹20,000 or higher follows the third rule.

Do not convert another currency, an annual figure, or an hourly figure into a monthly INR amount. If the posting does not state a monthly INR range, do not apply the ₹20,000 floor by estimation. Route that posting to review when a salary decision cannot be made from the stated text.

For international roles, evaluate a disclosed salary against the prevailing market range for the role and location. Do not apply the ₹20,000/month floor by converting foreign pay into INR. If the international salary is undisclosed, do not automatically reject solely because salary is unknown.

If a mandatory salary field must be answered, use the exact India or international answer in `config/answer_bank.md`. Do not substitute a number that is not in that answer.

## Work schedule

PREFERRED_SHIFTS=Day
MAX_WORKDAYS_PER_WEEK=5
ACCEPT_NIGHT_SHIFTS=YES_ONLY_IF_FULLY_REMOTE
ACCEPT_ROTATIONAL_SHIFTS=YES_ONLY_IF_FULLY_REMOTE
AVAILABILITY=Immediately

Day shift is the preferred shift for remote, hybrid, and on-site roles.
Night shift is acceptable only when the role is fully remote.
Rotational shift is acceptable only when the role is fully remote.
Reject a night-shift or rotational-shift role that is on-site or hybrid.
Reject a role that requires more than 5 workdays per week.
If the shift or workweek is not stated, do not assume a day shift or a 5-day week, and do not reject the role solely because the schedule is unknown.

## Work authorization

INDIA_WORK_AUTHORIZATION=AUTHORIZED_TO_WORK_IN_INDIA
INTERNATIONAL_WORK_AUTHORIZATION=NONE
INTERNATIONAL_VISA_OR_PERMIT=NONE
SPONSORSHIP_REQUIRED_WHERE_EMPLOYER_SPONSORSHIP_IS_REQUIRED=YES

The candidate is authorized to work in India.
The candidate has no current international work authorization.
International opportunities may require employer-sponsored work authorization.
For countries where employer sponsorship is required, the candidate may require employer-sponsored work authorization.
Never claim existing international work authorization.
Never claim an existing visa or permit.
Use the exact answers in `config/answer_bank.md`.

## Job sources

Discover roles from multiple relevant sources in each run. Do not rely primarily on Internshala. Internshala is only one supplemental source for India fresher and internship listings.

Attempt these sources when the site permits ordinary search under `config/site_policy.md`:

- LinkedIn Jobs
- Naukri
- Indeed, including the India edition and the editions for the international target locations
- Google Jobs
- Direct employer career pages
- Public ATS listings, including Greenhouse, Lever, Ashby, and Workday career pages
- Glassdoor
- Foundit
- Shine
- Hirist
- Cutshort
- Internshala, as a supplemental India source only
- Bayt, GulfTalent, and Naukrigulf for Dubai
- Seek for Sydney
- Reed and Totaljobs for London
- Welcome to the Jungle for Paris and other suitable European locations
- Indeed Canada and LinkedIn for Toronto and Vancouver
- LinkedIn, Indeed, and Glassdoor for New York
- LinkedIn for Seoul, plus public listings on Saramin or JobKorea when the posting can be read without claiming language fluency

Use each source for discovery and verification. Prefer direct employer career pages and standard ATS pages when the same job appears on a board. If a source blocks automation or disallows it, record the reason and continue with the remaining sources. Do not create extra accounts, rotate identities, or bypass a restriction to reach a source.

## Application volume

The only numeric caps are in `config/runtime.md`:

MAX_APPLICATIONS_PER_RUN=5
MAX_APPLICATIONS_PER_DAY=10

Do not exceed these without an explicit edit to that file.

## Recruiter outreach

Disabled by default.
Do not send cold recruiter messages as part of this automation unless explicitly enabled.
