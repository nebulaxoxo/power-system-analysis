import re
import time
from datetime import datetime, timedelta

import pdfplumber

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# ============================================================
# CONFIGURATION
# ============================================================

PDF_PATH = r"D:\AMALGAMIST\Summer_Internship_Activity_Report_Final_Updated.pdf"

START_DATE = datetime(2026, 7, 1)
END_DATE   = datetime(2026, 7, 3)

# ============================================================
# EXTRACT ACTIVITIES FROM PDF
# ============================================================

activities = {}

date_pattern = re.compile(r'(\d{1,2})\s+(May|June|July)\s+2026')

month_map = {
    "May":5,
    "June":6,
    "July":7
}

print("Reading internship report...")

with pdfplumber.open(PDF_PATH) as pdf:

    for page in pdf.pages:

        tables = page.extract_tables()

        if not tables:
            continue

        for table in tables:

            for row in table:

                if not row or len(row) < 3:
                    continue

                row = [c if c else "" for c in row]

                date_cell = row[1]
                activity = row[2]

                m = date_pattern.search(date_cell)

                if not m:
                    continue

                day = int(m.group(1))
                month = month_map[m.group(2)]

                date = datetime(2026, month, day)

                activities[date.strftime("%d-%b-%Y")] = activity

print(f"Loaded {len(activities)} activity entries.")

# ============================================================
# FORMAT TEXT
# ============================================================

def format_text(text):

    if not text:
        return ""

    text = text.replace("\r", "")
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    bullets = []

    for part in text.split("●"):

        part = part.strip()

        if part:
            bullets.append("● " + part)

    text = "\n\n".join(bullets)

    # stay below textbox limit
    if len(text) > 995:
        text = text[:995]

        last = text.rfind("●")

        if last > 0:
            text = text[:last].rstrip()

    return text

# ============================================================
# OPEN CHROME
# ============================================================

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)

driver.maximize_window()

print()
print("="*60)
print("1. Login to VTOP")
print("2. Navigate to the Daily Activity page")
print("3. Keep that page open")
print("="*60)

input("Press ENTER once the activity page is visible...")

wait = WebDriverWait(driver, 60)

# Wait until first textbox exists

wait.until(
    EC.presence_of_element_located(
        (By.ID, "R26-Jun-2026")
    )
)

print("Activity page detected.\n")

# ============================================================
# FILL
# ============================================================

current = START_DATE

total = (END_DATE - START_DATE).days + 1
count = 1

while current <= END_DATE:

    date_str = current.strftime("%d-%b-%Y")

    print(f"[{count}/{total}] {date_str}")

    if current.weekday() == 5:

        text = "Saturday - Not working."

    elif current.weekday() == 6:

        text = "Sunday - Not working."

    else:

        text = format_text(
            activities.get(date_str, "")
        )

    textarea_id = "R" + date_str

    textarea = wait.until(
        EC.presence_of_element_located(
            (By.ID, textarea_id)
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        textarea
    )

    textarea.clear()

    textarea.send_keys(text)

    add_button = textarea.find_element(
        By.XPATH,
        "./following::button[1]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        add_button
    )

    time.sleep(0.5)

    add_button.click()

    print("   ✓ Saved")

    time.sleep(1.5)

    current += timedelta(days=1)
    count += 1

print()
print("="*50)
print("Finished Successfully!")
print("="*50)

input("Press ENTER to close browser...")

driver.quit()