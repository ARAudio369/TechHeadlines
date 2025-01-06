import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random 

# Function to fetch the latest 'x' tech headlines from a specific URL and topic
def get_headlines_from_website(url, num_articles=5):
    headlines = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Handle TechCrunch - Looking for <a> tags with class 'loop-card__title-link'
            if 'techcrunch.com' in url:
                for article in soup.find_all('a', class_='loop-card__title-link', limit=num_articles):
                    headline = article.get_text(strip=True)  # Get the text of the <a> tag
                    link = article['href']  # Get the href attribute for the link
                    if headline and link:
                        headlines.append((headline, link))
                        
            # Handle Ars Technica - Looking for <a> tags with class 'text-gray-700'
            elif 'arstechnica.com' in url:
                for article in soup.find_all('a', class_='text-gray-700', limit=num_articles):
                    headline = article.get_text(strip=True)
                    link = article['href']
                    if headline and link:
                        headlines.append((headline, link))           
                        
            # Handle TechRadar - Looking for <a> tags with class 'article-link' and extract headline from <h3> tags with class 'article-name'
            elif 'techradar.com' in url:
                for article in soup.find_all('a', class_='article-link', limit=num_articles):
                    headline = article.find('h3', class_='article-name').get_text(strip=True) if article.find('h3', class_='article-name') else None
                    link = article['href']
                    if headline and link:
                        headlines.append((headline, link))

        else:
            print(f"Error: Unable to fetch headlines from {url}, status code {response.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

    return headlines


# Function to prepare email body with a mix of articles
def prepare_email_body(websites, num_articles=5):
    body = '<h1>Articles from This Week</h1>'
    all_articles = []

    # Fetch headlines from all websites
    for website in websites:
        headlines = get_headlines_from_website(website, num_articles)
        all_articles.extend(headlines)
    
    # Limit to a maximum of 5 articles, chosen randomly from latest ones
    random_articles = random.sample(all_articles, min(5, len(all_articles)))  # Randomly select from the latest articles

    if random_articles:
        for title, link in random_articles:
            body += f'<p><a href="{link}">{title}</a></p>'
    else:
        body += '<p>No articles found this week.</p>'
    
    return body


# Function to send email with headlines
def send_email(subject, body, to_email):
    from_email = 'your_email@example.com'  # Replace with your email
    password = 'your_password_here'  # Replace with your email password or app-specific password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Gmail SMTP server
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Main function
def main():
    websites = [
        'https://techcrunch.com/category/artificial-intelligence/',
        'https://arstechnica.com/ai/',
        'https://www.techradar.com/uk/computing/software/artificial-intelligence'
    ]
    
    subject = 'Latest Tech Articles'
    body = prepare_email_body(websites)
    recipient_email = 'recipient_email@example.com'  # Replace with recipient email
    send_email(subject, body, recipient_email)

# Run the script
if __name__ == '__main__':
    main()
