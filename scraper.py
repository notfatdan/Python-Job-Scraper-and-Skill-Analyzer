import argparse
from bs4 import BeautifulSoup, Tag
from selenium_setup import SeleniumScraper, Browsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import pyautogui
import time
import random
import pandas as pd


def random_wait(min_time=1, max_time=4):
    """Introduce a random delay between min_time and max_time seconds."""
    delay = random.uniform(min_time, max_time)
    print(f"Waiting for {round(delay, 2)} seconds...")
    time.sleep(delay)


def requires_human_verification(self):
    if "Verify" in str(self.driver.page_source):
        self.driver.fullscreen_window()
        time.sleep(2)
        where = {Browsers.FIREFOX: {"x": 537, "y": 286}}
        pyautogui.click(where[self.browser]["x"], where[self.browser]["y"])
        time.sleep(2)
        self.driver.minimize_window()
        return True
    else:
        return False


def get_data(scrape_url, scraper, max_pages):
    page = 1
    all_skills = []
    scraper.go_to_url(scrape_url)
    print("Navigating to the main job listings page...")
    random_wait(3, 6)

    while page <= max_pages:
        soup = BeautifulSoup(scraper.driver.page_source, "html.parser")
        jobs = soup.find_all("div", class_="job_seen_beacon")
        print(f"Found {len(jobs)} job listings on page {page}.")

        for index, job in enumerate(jobs):
            print(f"Processing job {index + 1} on page {page}...")

            try:
                job_title_element = scraper.driver.find_elements(
                    By.CLASS_NAME, "jcs-JobTitle"
                )[index]
                job_title_element.click()
                print(f"Clicked job {index + 1}")
                random_wait(3, 6)
            except Exception as e:
                print(f"Error clicking job {index + 1}: {e}")
                continue

            description_html = get_job_description(scraper)

            if description_html:
                skills = extract_skills(description_html)
            else:
                print(f"No description found for job {index + 1}, skipping...")
                skills = []

            print(f"Skills found in job {index + 1}: {skills}")
            all_skills.extend(skills)

            random_wait(2, 4)

        print("Finished processing the page.")
        if not click_next_page(scraper):
            break
        page += 1
        random_wait(2, 4)

    return all_skills


def get_job_description(scraper):

    try:
        WebDriverWait(scraper.driver, 10).until(
            EC.presence_of_element_located((By.ID, "jobDescriptionText"))
        )
        description_element = scraper.driver.find_element(By.ID, "jobDescriptionText")
        description_html = description_element.get_attribute("innerHTML")
        return description_html

    except TimeoutException:
        print("Timeout waiting for the job description panel.")
        return ""


def extract_skills(description_html):
    soup = BeautifulSoup(description_html, "html.parser")
    description_text = soup.get_text(separator=" ").strip()

    keywords = [
        "Python",
        "JavaScript",
        "TypeScript",
        "React",
        "Node.js",
        "Next.js",
        "Django",
        "React Native",
        "Java ",
        "C++",
        "C#",
        ".NET",
        "AWS",
        "Docker",
        "Kubernetes",
        "Front-End",
        "Backend",
        "Fullstack",
        "SQL",
        "NoSQL",
        "Mongo",
        "Go",
        "Rust",
        "Ruby",
        "Perl",
        "Swift",
        "Scala",
        "PHP",
        "Angular",
        "Vue",
        "Laravel",
        "Flask",
        "Spring Boot",
        "Express",
        "Linux",
    ]
    found_keywords = []
    for word in keywords:
        if word in description_text:
            found_keywords.append(word.strip())

    if found_keywords:
        print(f"Extracted skills: {found_keywords}")
    else:
        print("No skills found.")
    return found_keywords


def click_next_page(scraper):
    try:
        next_button = scraper.driver.find_element(
            By.CSS_SELECTOR, "a[data-testid='pagination-page-next']"
        )
        next_button.click()
        print("Moving to the next page...")
        time.sleep(random.uniform(2, 4))  # shorter wait now
        close_popup(scraper)
        return True
    except Exception as e:
        print(f"Error clicking next page: {e}")
        return False


def prepare_data(all_skills):
    skill_counts = Counter(all_skills)

    df = pd.DataFrame(skill_counts.items(), columns=["Skill", "Count"])

    return df


def visualize(skill_df):
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x="Skill", y="Count", data=skill_df.sort_values("Count", ascending=False)
    )

    plt.title("Most in Demand Skills for Software Engineers in the Sydney Region")
    plt.xlabel("Skill", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.show()


def clear_cookies(scraper):
    scraper.driver.delete_all_cookies()
    print("Cleared cookies to avoid CAPTCHA detection.")


def close_popup(scraper):
    try:
        print("Attempting to close popup...")
        close_button = scraper.driver.find_element(
            By.CSS_SELECTOR, 'button[aria-label="close"]'
        )
        close_button.click()
        time.sleep(1)
        print("Popup closed successfully.")
    except Exception as e:
        print(f"Failed to close popup: {e}")


def main():
    parser = argparse.ArgumentParser(description="Indeed Job Scraper")
    parser.add_argument("pages", type=int, help="Number of pages to scrape")
    args = parser.parse_args()

    max_pages = args.pages
    print("Starting the scraper...")

    random_wait(2, 5)

    scrape_url = "https://au.indeed.com/jobs?q=software+developer&l=Sydney+NSW&from=searchOnHP&vjk=3a82a1c0a89096eb"

    scraper = SeleniumScraper(browser=Browsers.FIREFOX)
    scraper.open_browser()
    clear_cookies(scraper)

    all_skills = get_data(scrape_url, scraper, max_pages)

    scraper.close_browser()

    skill_df = prepare_data(all_skills)
    visualize(skill_df)


if __name__ == "__main__":
    main()
