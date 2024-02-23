# MAIN CODE
import re
import html
import schedule
import time
import xml.etree.ElementTree as ET
import requests


def format_description(text):
  new = re.sub('<.*?>', '', text)
  pattern = r'Posted On: [^<]+'
  cleaned_text = re.sub(pattern, '', new)
  cleaned_text = html.unescape(cleaned_text)

  return cleaned_text

print("""

██     ██ ███████ ██       ██████  ██████  ███    ███ ███████     ████████  ██████      ██    ██ ██████  ████████ ██████   █████   ██████ ██   ██ 
██     ██ ██      ██      ██      ██    ██ ████  ████ ██             ██    ██    ██     ██    ██ ██   ██    ██    ██   ██ ██   ██ ██      ██  ██  
██  █  ██ █████   ██      ██      ██    ██ ██ ████ ██ █████          ██    ██    ██     ██    ██ ██████     ██    ██████  ███████ ██      █████   
██ ███ ██ ██      ██      ██      ██    ██ ██  ██  ██ ██             ██    ██    ██     ██    ██ ██         ██    ██   ██ ██   ██ ██      ██  ██  
 ███ ███  ███████ ███████  ██████  ██████  ██      ██ ███████        ██     ██████       ██████  ██         ██    ██   ██ ██   ██  ██████ ██   ██ 
                                                                                                                                                  
                                                                                                                                                  

""")

email = input('Please enter your Email :')
rss = input('Please enter your RSS URL :')


# Set to store unique job IDs
processed_job_ids = set() # clean this set to just 10 items

def fetch_xml_data():
    # URL of the RSS feed
    rss_url = f"{rss}"

    # Fetch the XML data from the RSS feed
    response = requests.get(rss_url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch XML data from the RSS feed")
        return None

def parse_xml(xml_data):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Initialize a list to store job information
    jobs = []

    # Iterate over each <item> element in the XML
    for item in root.findall('.//item'):
        job = {}

        # Extract job details
        job['title'] = item.find('title').text.strip()
        job['link'] = item.find('link').text.strip()
        job['description'] = item.find('description').text.strip()
        job['job_id'] = item.find('guid').text.strip()  # Assuming the <guid> tag contains a unique job ID

        # Check if job ID has already been processed
        if job['job_id'] in processed_job_ids:
            continue

        # Extract additional job details
        additional_details = item.find('description').text.strip().split('<br />')
        for detail in additional_details:
            if 'Posted On' in detail:
                posted_on = detail.split(': ')
                if len(posted_on) > 1:
                    job['posted_on'] = posted_on[1]
            elif 'Category' in detail:
                category = detail.split(': ')
                if len(category) > 1:
                    job['category'] = category[1]
            elif 'Country' in detail:
                country = detail.split(': ')
                if len(country) > 1:
                    job['country'] = country[1]
            elif 'Budget' in detail:
                budget = detail.split(': ')
                if len(budget) > 1:
                    job['budget'] = budget[1]
            elif 'Hourly Range' in detail:
                rate = detail.split(': ')
                if len(rate) > 1:
                    job['rate'] = rate[1]



        # Add job ID to the set of processed job IDs
        processed_job_ids.add(job['job_id'])

        # Add job to the list
        jobs.append(job)

    return jobs

def print_jobs(jobs):
    # Print the job details in a readable format
    for job in jobs[:1]:
        print(f"Title: {job['title']}")
        print(f"Link: {job['link']}")
        print(f"Description: {format_description(job['description'])}")
        #processed_description = process_description(description)


        #print(f"Publication Date: {job['pubDate']}")
        if 'posted_on' in job:
            print(f"Posted On: {job['posted_on']}")
        if 'category' in job:
            print(f"Category: {job['category']}")
        if 'budget' in job:
            print(f"Budget: {job['budget']}")
        if 'country' in job:
            print(f"Country: {job['country']}")
        if 'rate' in job:
            print(f"Budget: {job['rate']}")


        print("----------------------------------------------------------------------------------------")

def job():
    # Fetch XML data from the RSS feed
    xml_data = fetch_xml_data()
    if xml_data:
        # Parse XML and print jobs
        jobs = parse_xml(xml_data)
        print_jobs(jobs)
    else:
        print("Failed to fetch XML data")

schedule.every().second.do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(3)