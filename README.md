# Job Scraper Project

## Overview

This project is a web scraper built using Python, Selenium, and BeautifulSoup to scrape job listings for software engineering roles from Indeed in Sydney, Australia. It extracts in-demand skills and visualizes the data using Seaborn.

## Features

- Scrapes multiple pages of job listings from Indeed
- Extracts key skills from job descriptions
- Random wait times to mimic human behavior and avoid bot detection
- Visualizes in-demand skills using Seaborn

## Requirements

To run this project, you'll need to install the dependencies listed in `requirements.txt`. You can install them with:

```bash
pip install -r requirements.txt
```

1. Clone the repo

```bash
git clone https://github.com/yourusername/job-scraper.git
```

2. Navigate to the project directory

```bash
cd job-scraper
```

3. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

To run the scraper, use the following command

```bash
python scraper.py <number_of_pages>
```

Example

```bash
python scraper.py 3
```

## Demo


https://github.com/user-attachments/assets/98167f91-6bc9-4756-803a-82696b31a782



This project is licensed under the MIT License. See the LICENSE file for details.
