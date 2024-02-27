# MAIN CODE
import re
import html
import schedule
import time
import xml.etree.ElementTree as ET
import requests
import sys
from send_mail import send_mail
import markdown


def format_description(text):
  new = re.sub('<.*?>', '', text)
  pattern = r'Posted On: [^<]+'
  cleaned_text = re.sub(pattern, '', new)
  cleaned_text = html.unescape(cleaned_text)

  return cleaned_text

# Set to store unique job IDs
processed_job_ids = []

def fetch_xml_data(rss):
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

    # Ensure only up to 5 jobs are stored
    while len(jobs) >= 5:
        # print('max jobs reached for the list')
        jobs.pop(-1) 
        # print('last job removed len of list is', len(jobs))
        

    # Iterate over each <item> element in the XML
    for item in root.findall('.//item'):
        job = {}

        # Extract job details
        job['title'] = item.find('title').text.strip()
        job['title'] = html.unescape(job['title'])
        job['link'] = item.find('link').text.strip()
        job['description'] = item.find('description').text.strip()
        job['job_id'] = item.find('guid').text.strip()  # Assuming the <guid> tag contains a unique job ID

        # Check if job ID has already been processed
        if job['job_id'] in processed_job_ids:
            continue

        # Ensure only up to 5 processed job IDs are stored
        while len(processed_job_ids) >= 5:
            # print('len of Job IDs has exceeded 5')
            processed_job_ids.pop(-1)
            # print('last job removed , len of list is ',len(processed_job_ids))

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
                    job['rate'] = rate[1] +" hourly"
            else:
                job['non'] = 'Hourly, Not Specified'
                

        # Add job ID to the set of processed job IDs
        processed_job_ids.append(job['job_id'])

        # Add job to the list
        jobs.append(job)

    return jobs



prev_job = {}  # Initialize outside the function

def get_budget(job):
    if 'budget' in job:
        return job['budget']
    elif 'rate' in job:
        return job['rate']
    elif 'non' in job:
        return job['non']
    else:
        return "Not specified"

def job(email, rss_url):
    global processed_job_ids  # Access the global variable
    global prev_job

    xml_data = fetch_xml_data(rss_url)
    if xml_data:
        jobs = parse_xml(xml_data)
        new_job = jobs[0] 
        if new_job != prev_job:
            body = f"""
            🚨 New Job Available 🚨

            <b>Title</b>: {new_job['title']}<br>
            <b>Description</b>: {format_description(new_job['description'])}<br>
            <b>Posted On</b>: {new_job['posted_on']}<br>
            <b>Category</b>: {new_job['category']}<br>
            <b>Budget</b>: {get_budget(new_job)}<br>
            <b>Client Country</b>: {new_job['country']}<br>
            <b>APPLY HERE</b>: <a href="{new_job['link']}">Link to Apply</a><br>
            """

            # Remove leading whitespace from each line
            body = '\n'.join(line.strip() for line in body.split('\n'))
                    
            send_mail(email,body)
            prev_job = new_job
        else:
            print('No new job')
    else:
        print("Failed to fetch XML data")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <email> <rss_url>")
        sys.exit(1)

    email = sys.argv[1]
    rss_url = sys.argv[2]
    prev_job = None

    job(email, rss_url)
    schedule.every().second.do(job, email, rss_url)
    failed_process = []
    while True:
        try:
            schedule.run_pending()
            time.sleep(3)
            if failed_process:
                failed_process.pop(0)
        except Exception as e:
            failed_process.append(1)


            