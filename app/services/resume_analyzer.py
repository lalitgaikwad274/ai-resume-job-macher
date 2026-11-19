import re
from datetime import datetime

MONTH_DICT = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

month_re = r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
dash_re = r"(?:\s*[-–—·to]+\s*|\s+to\s+)"
present_re = r"(?:present|current|till\s+date|now)"

# Date range pattern supporting MM/YYYY, Month YYYY, and YYYY with Unicode dashes
DATE_RANGE_PATTERN = re.compile(
    rf"(?:"
    rf"(\d{{1,2}}/\d{{4}}){dash_re}(\d{{1,2}}/\d{{4}}|{present_re})?"
    rf"|"
    rf"({month_re}\.?\s+\d{{4}}){dash_re}({month_re}\.?\s+\d{{4}}|{present_re})?"
    rf"|"
    rf"(\b(?:19|20)\d{{2}}){dash_re}(\b(?:19|20)\d{{2}}|{present_re})"
    rf")",
    re.IGNORECASE,
)


def _parse_date_token(token: str) -> tuple[int, int]:
    """Parse a date string into (year, month). Defaults to current date for 'present'."""
    now = datetime.now()
    if not token:
        return now.year, now.month

    token = token.strip().lower()
    if re.search(present_re, token):
        return now.year, now.month

    m_mm_yyyy = re.match(r"(\d{1,2})/(\d{4})", token)
    if m_mm_yyyy:
        return int(m_mm_yyyy.group(2)), int(m_mm_yyyy.group(1))

    m_month_yyyy = re.match(rf"({month_re})\.?\s+(\d{{4}})", token)
    if m_month_yyyy:
        m_str = m_month_yyyy.group(1).lower()
        m_num = MONTH_DICT.get(m_str[:3], 1)
        return int(m_month_yyyy.group(2)), m_num

    m_yyyy = re.match(r"\b((?:19|20)\d{2})\b", token)
    if m_yyyy:
        return int(m_yyyy.group(1)), 1

    return now.year, now.month


def extract_experience(text: str) -> list:
    """Find experience duration mentions and date range calculations."""
    matches = []

    # 1. Explicit mentions (e.g. '5+ years of experience', 'Total experience: 4.5 years')
    explicit_patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience",
        r"(?:(?:\b(?:over|more\s+than|around|about|approx(?:\.|imately)?|at\s+least))\s+)?(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:work|professional|relevant|industry|hands-on\s+)?(?:experience|exp)",
        r"(?:total|overall|work)?\s*experience\s*(?:is|of|:)?\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+in\s+[a-zA-Z\s]{2,30}",
    ]

    for p in explicit_patterns:
        for found in re.findall(p, text, re.IGNORECASE):
            val = found if isinstance(found, str) else found[0]
            if val and val not in matches:
                matches.append(val)

    # 2. Date ranges in experience section
    # Separate sections to avoid counting university education dates as job experience
    sections = re.split(r"\n(?=[A-Z\s]{3,25}:?\n)", text)
    exp_text = ""
    for sec in sections:
        header = sec.strip().split("\n")[0].lower()
        if any(h in header for h in ["experience", "employment", "work history"]):
            exp_text += "\n" + sec

    target = exp_text if exp_text else text
    total_months = 0

    for m in DATE_RANGE_PATTERN.finditer(target):
        if not exp_text:
            context = target[max(0, m.start() - 50):m.end() + 50].lower()
            if any(edu in context for edu in ["college", "university", "bachelor", "master", "school", "degree"]):
                continue

        groups = [g for g in m.groups() if g]
        if groups:
            start_token = groups[0]
            end_token = groups[1] if len(groups) > 1 else "present"
            s_year, s_month = _parse_date_token(start_token)
            e_year, e_month = _parse_date_token(end_token)
            duration = (e_year - s_year) * 12 + (e_month - s_month)
            if 1 <= duration <= 480:
                total_months += duration

    if total_months > 0:
        years = round(total_months / 12, 1)
        years_str = str(int(years)) if years.is_integer() else str(years)
        if years_str not in matches:
            matches.append(years_str)

    return list(dict.fromkeys(matches))


DEGREE_PATTERNS = [
    r"Master\s+of\s+Computer\s+Science",
    r"Bachelor\s+of\s+Computer\s+Science",
    r"Bachelor\s+of\s+Technology",
    r"Master\s+of\s+Technology",
    r"Bachelor\s+of\s+Engineering",
    r"Master\s+of\s+Engineering",
    r"Bachelor\s+of\s+Computer\s+Applications",
    r"Master\s+of\s+Computer\s+Applications",
    r"Bachelor\s+of\s+Science\s+in\s+Computer\s+Science",
    r"Master\s+of\s+Science\s+in\s+Computer\s+Science",
    r"Bachelor\s+of\s+Science\s+in\s+Information\s+Technology",
    r"Master\s+of\s+Science\s+in\s+Information\s+Technology",
    r"Bachelor\s+of\s+Information\s+Technology",
    r"Master\s+of\s+Information\s+Technology",
    r"Bachelor\s+of\s+Science",
    r"Master\s+of\s+Science",
    r"Bachelor\s+of\s+Commerce",
    r"Master\s+of\s+Commerce",
    r"Bachelor\s+of\s+Arts",
    r"Master\s+of\s+Arts",
    r"Bachelor\s+of\s+Business\s+Administration",
    r"Master\s+of\s+Business\s+Administration",
    r"Bachelor\s+of\s+Management\s+Studies",
    r"Bachelor\s+of\s+Laws",
    r"Master\s+of\s+Laws",
    r"Bachelor\s+of\s+Pharmacy",
    r"Master\s+of\s+Pharmacy",
    r"Bachelor\s+of\s+Architecture",
    r"Master\s+of\s+Architecture",
    r"Bachelor\s+of\s+Design",
    r"Master\s+of\s+Design",
    r"Bachelor's\s+Degree",
    r"Master's\s+Degree",
    r"Doctor\s+of\s+Philosophy",
    r"B\.?\s*Tech",
    r"M\.?\s*Tech",
    r"B\.?\s*E\.?",
    r"M\.?\s*E\.?",
    r"BCA",
    r"MCA",
    r"B\.?\s*Sc\.?",
    r"M\.?\s*Sc\.?",
    r"B\.?\s*Com\.?",
    r"M\.?\s*Com\.?",
    r"BBA",
    r"MBA",
    r"B\.?\s*S\.?",
    r"M\.?\s*S\.?",
    r"Ph\.?\s*D\.?",
    r"Diploma(?:\s+in\s+[a-zA-Z\s]+)?",
    r"PGDM",
]

degree_regex = re.compile(
    r"\b(" + "|".join(sorted(DEGREE_PATTERNS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

# Date pattern that matches full ranges or open-ended ranges (e.g. 07/2020 – 05/2022, 07/2017 –)
date_regex = re.compile(
    r"\b(?:0?[1-9]|1[0-2])?/?(?:19|20)\d{2}\s*(?:[-–—to]+\s*(?:Present|Current|(?:0?[1-9]|1[0-2])?/?(?:19|20)\d{2})?)?",
    re.IGNORECASE,
)


def extract_education(text: str) -> list:
    """Extract education details (degree, institution, dates) from resume text."""
    # Collapse multiple whitespaces and newlines so wrapped titles like 'Master of Computer\nScience' match
    normalized_text = re.sub(r"\s+", " ", text).strip()

    matches = list(degree_regex.finditer(normalized_text))
    education = []

    for i, match in enumerate(matches):
        degree = match.group(0).strip()
        start_pos = match.end()
        # Bound the segment to where the next degree begins to prevent bleeding
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(normalized_text)
        segment = normalized_text[start_pos:end_pos].strip()

        # Find date within this segment
        date_match = date_regex.search(segment)
        dates = None
        institution = segment

        if date_match:
            dates = date_match.group(0).strip(" ·,-–—")
            institution = segment[:date_match.start()].strip()

        institution = institution.strip(" ·,-–—\t")
        if not institution:
            institution = None

        education.append({
            "degree": degree,
            "institution": institution,
            "dates": dates,
        })

    return education
