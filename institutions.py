# ============================================
# StudyMate AI - Pakistani Institutions Data
# All Universities, Boards, Testing Authorities
# ============================================

# ============================================
# FEDERAL & NATIONAL BODIES
# ============================================

TESTING_AUTHORITIES = [
    "PMC (Pakistan Medical Commission)",
    "HEC (Higher Education Commission)",
    "NTS (National Testing Service)",
    "ETEA (Educational Testing & Evaluation Agency)",
    "BISE Federal (FBISE)",
    "PEC (Pakistan Engineering Council)",
    "PNC (Pakistan Nursing Council)",
    "PMDC (Pakistan Medical & Dental Council)",
    "PPSC (Punjab Public Service Commission)",
    "FPSC (Federal Public Service Commission)",
    "SPSC (Sindh Public Service Commission)",
    "KPPSC (KPK Public Service Commission)",
    "BPSC (Balochistan Public Service Commission)",
    "AJKPSC (AJK Public Service Commission)",
    "IBA Sukkur (NTS Partner)",
    "CTS (Career Testing Service)",
    "OTS (Online Testing Service)",
]

# ============================================
# BOARDS OF INTERMEDIATE & SECONDARY EDUCATION
# ============================================

BOARDS = {
    "Federal": [
        "Federal Board of Intermediate & Secondary Education (FBISE)",
    ],

    "Punjab": [
        "BISE Lahore",
        "BISE Rawalpindi",
        "BISE Gujranwala",
        "BISE Faisalabad",
        "BISE Multan",
        "BISE Sahiwal",
        "BISE Sargodha",
        "BISE DG Khan (Dera Ghazi Khan)",
        "BISE Bahawalpur",
    ],

    "Sindh": [
        "BISE Karachi",
        "BISE Hyderabad",
        "BISE Sukkur",
        "BISE Larkana",
        "BISE Mirpurkhas",
        "BISE Shaheed Benazirabad (Nawabshah)",
    ],

    "KPK": [
        "BISE Peshawar",
        "BISE Mardan",
        "BISE Abbottabad",
        "BISE Swat",
        "BISE Kohat",
        "BISE Bannu",
        "BISE Malakand",
        "BISE Dir (Lower)",
    ],

    "Balochistan": [
        "BISE Quetta",
        "BISE Turbat",
        "BISE Loralai",
        "BISE Khuzdar",
    ],

    "AJK": [
        "BISE Mirpur (AJK)",
        "BISE Muzaffarabad (AJK)",
        "BISE Rawalakot (AJK)",
    ],

    "Gilgit-Baltistan": [
        "BISE Gilgit-Baltistan",
    ],
}

# Flat list for dropdowns
BOARDS_FLAT = (
    ["── Federal ──", "Federal Board of Intermediate & Secondary Education (FBISE)"]
    + ["── Punjab ──"] + BOARDS["Punjab"]
    + ["── Sindh ──"] + BOARDS["Sindh"]
    + ["── KPK ──"] + BOARDS["KPK"]
    + ["── Balochistan ──"] + BOARDS["Balochistan"]
    + ["── AJK ──"] + BOARDS["AJK"]
    + ["── Gilgit-Baltistan ──"] + BOARDS["Gilgit-Baltistan"]
    + ["Other Board"]
)


# ============================================
# UNIVERSITIES — BY CATEGORY
# ============================================

UNIVERSITIES = {

    "Medical & Health Sciences": [
        "NUMS (National University of Medical Sciences)",
        "King Edward Medical University (KEMU) Lahore",
        "Dow University of Health Sciences Karachi",
        "Aga Khan University Karachi",
        "Allama Iqbal Medical College Lahore",
        "Rawalpindi Medical University (RMU)",
        "Army Medical College (AMC) Rawalpindi",
        "Fatima Jinnah Medical University Lahore",
        "University of Health Sciences (UHS) Lahore",
        "Shifa College of Medicine Islamabad",
        "CMH Lahore Medical College",
        "Foundation University Medical College Islamabad",
        "Khyber Medical University (KMU) Peshawar",
        "Liaquat University of Medical & Health Sciences (LUMHS) Jamshoro",
        "Shaikh Khalifa Bin Zayed Al-Nahyan Medical & Dental College Lahore",
        "Quaid-e-Azam Medical College Bahawalpur",
        "Nishtar Medical University Multan",
        "Gujranwala Medical College",
        "Sahiwal Medical College",
        "Faisalabad Medical University",
        "Azra Naheed Medical College Lahore",
        "Central Park Medical College Lahore",
        "Pak Red Crescent Medical & Dental College Lahore",
        "Islam Medical College Sialkot",
        "Avicenna Medical College Lahore",
        "Ibn Sina Medical College Multan",
        "Rahbar Medical & Dental College Lahore",
        "Services Institute of Medical Sciences (SIMS) Lahore",
    ],

    "Engineering & Technology": [
        "NUST (National University of Sciences & Technology) Islamabad",
        "UET Lahore (University of Engineering & Technology)",
        "UET Peshawar",
        "UET Taxila",
        "NED University Karachi",
        "PIEAS (Pakistan Institute of Engineering & Applied Sciences)",
        "COMSATS University Islamabad",
        "COMSATS University Lahore",
        "COMSATS University Wah",
        "COMSATS University Abbottabad",
        "COMSATS University Attock",
        "COMSATS University Sahiwal",
        "COMSATS University Vehari",
        "FAST-NUCES Islamabad",
        "FAST-NUCES Lahore",
        "FAST-NUCES Karachi",
        "FAST-NUCES Peshawar",
        "FAST-NUCES Chiniot-Faisalabad",
        "Mehran University Jamshoro",
        "Dawood University Karachi",
        "Sir Syed University Karachi",
        "Institute of Space Technology (IST) Islamabad",
        "Pakistan Navy Engineering College (PNEC) Karachi",
        "Military College of Engineering (MCE) Risalpur",
        "College of Electrical & Mechanical Engineering (CEME) Rawalpindi",
        "Ghulam Ishaq Khan (GIK) Institute Topi",
        "University of Engineering & Technology (UET) Mardan",
        "Balochistan University of Engineering & Technology Khuzdar",
        "Quetta Institute of Medical Sciences (QIMS)",
        "Hamdard University Karachi",
    ],

    "General / Public Universities": [
        "Quaid-i-Azam University (QAU) Islamabad",
        "University of the Punjab Lahore",
        "University of Karachi",
        "University of Peshawar",
        "University of Balochistan Quetta",
        "Bahauddin Zakariya University (BZU) Multan",
        "University of Agriculture Faisalabad (UAF)",
        "University of Sargodha",
        "Government College University (GCU) Lahore",
        "Government College University (GCU) Faisalabad",
        "Forman Christian College University Lahore",
        "University of Gujrat",
        "University of Sialkot",
        "Islamia University of Bahawalpur (IUB)",
        "University of Education Lahore",
        "Minhaj University Lahore",
        "University of Lahore",
        "Superior University Lahore",
        "University of Central Punjab (UCP) Lahore",
        "Lahore Leads University",
        "University of South Asia Lahore",
        "Riphah International University Islamabad",
        "Shaheed Zulfikar Ali Bhutto Institute of Science & Technology (SZABIST)",
        "Institute of Business Administration (IBA) Karachi",
        "IBA Sukkur",
        "Sukkur IBA University",
        "Shah Abdul Latif University Khairpur",
        "University of Sindh Jamshoro",
        "Liaquat University Hyderabad",
        "University of the Punjab Gujranwala Campus",
        "Abdul Wali Khan University Mardan",
        "Hazara University Mansehra",
        "University of Swat",
        "University of Malakand",
        "Bacha Khan University Charsadda",
        "University of Haripur",
        "Islamia College University Peshawar",
        "Kohat University of Science & Technology (KUST)",
        "Gomal University DI Khan",
        "University of Science & Technology Bannu",
        "Women University Swabi",
        "Women University Mardan",
        "University of Azad Jammu & Kashmir (UAJK) Muzaffarabad",
        "Mirpur University of Science & Technology (MUST)",
        "University of Kotli AJK",
        "Karakoram International University (KIU) Gilgit",
        "University of Gwadar",
        "Lasbela University Uthal",
        "Turbat University",
    ],

    "Business & Management": [
        "Lahore University of Management Sciences (LUMS)",
        "Institute of Business Administration (IBA) Karachi",
        "Institute of Business Management (IoBM) Karachi",
        "Pakistan Institute of Development Economics (PIDE) Islamabad",
        "Shaheed Zulfikar Ali Bhutto Institute of Science & Technology (SZABIST) Islamabad",
        "Bahria University Islamabad",
        "Air University Islamabad",
        "Virtual University of Pakistan (VU)",
        "Preston University",
        "Iqra University Islamabad",
        "Iqra University Karachi",
        "Greenwich University Karachi",
        "CBM (College of Business Management) Karachi",
        "Karachi School of Business & Leadership (KSBL)",
        "Beacon House National University Lahore",
    ],

    "Agriculture & Veterinary": [
        "University of Agriculture Faisalabad (UAF)",
        "PMAS-Arid Agriculture University Rawalpindi",
        "Sindh Agriculture University Tandojam",
        "Agriculture University Peshawar",
        "Lasbela University of Agriculture Water & Marine Sciences",
        "University of Veterinary & Animal Sciences (UVAS) Lahore",
        "Cholistan University of Veterinary & Animal Sciences Bahawalpur",
        "Shaheed Benazir Bhutto University of Veterinary & Animal Sciences Sakrand",
    ],

    "Islamic & Religious": [
        "International Islamic University Islamabad (IIUI)",
        "Allama Iqbal Open University (AIOU) Islamabad",
        "University of Faisalabad (Islamic Studies)",
        "Jamia Uloom-ul-Islamia",
        "Wifaq ul Madaris Al Arabia Pakistan",
        "Tanzeem-ul-Madaris Ahle Sunnat Pakistan",
        "Rabita-tul-Madaris Al-Islamia Pakistan",
    ],

    "Distance & Online": [
        "Virtual University of Pakistan (VU)",
        "Allama Iqbal Open University (AIOU) Islamabad",
        "SALU (Shah Abdul Latif University) Distance Learning",
    ],
}

# Flat list for dropdowns
UNIVERSITIES_FLAT = ["General / Any University"]
for category, unis in UNIVERSITIES.items():
    UNIVERSITIES_FLAT.append(f"── {category} ──")
    UNIVERSITIES_FLAT.extend(unis)
UNIVERSITIES_FLAT.append("Other University")


# ============================================
# ENTRY TESTS WITH INSTITUTIONS
# ============================================

ENTRY_TESTS = {
    "Medical": [
        "MDCAT (PMC — All Medical Colleges)",
        "NUMS Entry Test (Military Medical Colleges)",
        "Aga Khan University Entry Test (AKU-EAP)",
        "UHS Entry Test (University of Health Sciences)",
        "Khyber Medical University (KMU) Entry Test",
        "LUMHS Entry Test",
        "Bolan Medical College Entry Test",
    ],

    "Engineering": [
        "ECAT (UET — Engineering Colleges Punjab)",
        "NET-1 (NUST Entry Test — Round 1)",
        "NET-2 (NUST Entry Test — Round 2)",
        "NET-3 (NUST Entry Test — Round 3)",
        "GIKI Entry Test",
        "PIEAS Entry Test",
        "NED Entry Test",
        "Mehran University Entry Test",
    ],

    "Business / General": [
        "SAT (LUMS)",
        "IBA Entry Test Karachi",
        "IBA Sukkur Entry Test",
        "SZABIST Entry Test",
        "Bahria University Entry Test",
        "Air University Entry Test",
    ],

    "Computer Science": [
        "FAST Entry Test (NUCES)",
        "COMSATS Entry Test",
        "Virtual University Entry Test",
    ],

    "NTS Based": [
        "NTS-GAT (General)",
        "NTS-GAT (Subject)",
        "NTS-NAT (National Aptitude Test)",
        "NTS-HAT (Higher Achievement Test)",
        "OTS Entry Test",
        "CTS Entry Test",
        "ETEA Entry Test (KPK)",
    ],

    "CSS / PMS / Public Service": [
        "CSS (Central Superior Services) — FPSC",
        "PMS (Provincial Management Services) — PPSC",
        "PMS (KPK) — KPPSC",
        "PMS (Sindh) — SPSC",
        "PMS (Balochistan) — BPSC",
        "PMS (AJK) — AJKPSC",
        "Police Service Test",
        "Military Intelligence Tests",
    ],
}

ENTRY_TESTS_FLAT = []
for category, tests in ENTRY_TESTS.items():
    ENTRY_TESTS_FLAT.append(f"── {category} ──")
    ENTRY_TESTS_FLAT.extend(tests)
ENTRY_TESTS_FLAT.append("Other Entry Test")


# ============================================
# PROGRAMS / DEGREES
# ============================================

PROGRAMS = {
    "Medical & Health": [
        "MBBS (Bachelor of Medicine & Surgery)",
        "BDS (Bachelor of Dental Surgery)",
        "Pharm-D (Doctor of Pharmacy)",
        "DPT (Doctor of Physical Therapy)",
        "BSN Nursing (Generic — 4 Year)",
        "BSN Nursing (Post RN Bridge — 2 Year)",
        "BS MLT (Medical Lab Technology)",
        "BS Radiology & Imaging",
        "BS Anesthesia",
        "BS Dental Technology",
        "BS Optometry",
        "BS Nutrition & Dietetics",
        "BS Public Health",
        "BS Biotechnology",
        "Doctor of Veterinary Medicine (DVM)",
    ],

    "Engineering": [
        "BE / BSc Civil Engineering",
        "BE / BSc Electrical Engineering",
        "BE / BSc Mechanical Engineering",
        "BE / BSc Chemical Engineering",
        "BE / BSc Computer Engineering",
        "BE / BSc Software Engineering",
        "BE / BSc Telecom Engineering",
        "BE / BSc Industrial Engineering",
        "BE / BSc Environmental Engineering",
        "BE / BSc Petroleum Engineering",
        "BE / BSc Mining Engineering",
        "BE / BSc Aerospace Engineering",
        "DAE Civil Engineering",
        "DAE Electrical Engineering",
        "DAE Mechanical Engineering",
        "DAE Computer Information Technology (CIT)",
        "DAE Electronics",
        "DAE Chemical Engineering",
        "DAE Automobile Engineering",
        "DAE Architecture",
    ],

    "Computer & IT": [
        "BS Computer Science (BSCS)",
        "BS Software Engineering (BSSE)",
        "BS Information Technology (BSIT)",
        "BS Artificial Intelligence (BSAI)",
        "BS Data Science",
        "BS Cyber Security",
        "BS Computer Engineering",
        "MCS (Master of Computer Science)",
        "MIT (Master of Information Technology)",
        "MS Computer Science",
    ],

    "Business": [
        "BBA (Bachelor of Business Administration)",
        "BS Commerce (BCom)",
        "BS Accounting & Finance",
        "BS Economics",
        "MBA (Master of Business Administration)",
        "MS Finance",
        "CA (Chartered Accountancy — ICAP)",
        "ACCA (Association of Chartered Certified Accountants)",
        "CMA (Cost & Management Accountancy)",
        "CFA (Chartered Financial Analyst)",
    ],

    "Science": [
        "FSc Pre-Medical",
        "FSc Pre-Engineering",
        "BS Physics",
        "BS Chemistry",
        "BS Biology (Zoology / Botany)",
        "BS Mathematics",
        "BS Statistics",
        "BS Environmental Sciences",
        "BS Microbiology",
        "BS Biochemistry",
        "BS Genetics",
    ],

    "Social Sciences & Humanities": [
        "BA / BSc General",
        "BS English Literature",
        "BS Urdu",
        "BS Islamic Studies",
        "BS Pakistan Studies",
        "BS Psychology",
        "BS Sociology",
        "BS Education (BEd)",
        "BS Law (LLB)",
        "BS Political Science",
        "BS International Relations",
        "BS Media Studies / Mass Communication",
        "BS Fine Arts",
    ],

    "Agriculture": [
        "BS Agriculture",
        "BS Horticulture",
        "BS Agricultural Engineering",
        "BS Food Science & Technology",
        "BS Forestry",
        "BS Animal Husbandry",
    ],
}

PROGRAMS_FLAT = []
for category, progs in PROGRAMS.items():
    PROGRAMS_FLAT.append(f"── {category} ──")
    PROGRAMS_FLAT.extend(progs)
PROGRAMS_FLAT.append("Other Program")


def get_boards_flat():
    return BOARDS_FLAT

def get_universities_flat():
    return UNIVERSITIES_FLAT

def get_entry_tests_flat():
    return ENTRY_TESTS_FLAT

def get_programs_flat():
    return PROGRAMS_FLAT

def get_testing_authorities():
    return TESTING_AUTHORITIES

def search_institution(query, category="all"):
    """Search institutions by name"""
    query = query.lower()
    results = []

    if category in ("all", "university"):
        for cat, unis in UNIVERSITIES.items():
            for u in unis:
                if query in u.lower():
                    results.append(("University", cat, u))

    if category in ("all", "board"):
        for region, boards in BOARDS.items():
            for b in boards:
                if query in b.lower():
                    results.append(("Board", region, b))

    if category in ("all", "test"):
        for cat, tests in ENTRY_TESTS.items():
            for t in tests:
                if query in t.lower():
                    results.append(("Entry Test", cat, t))

    return results