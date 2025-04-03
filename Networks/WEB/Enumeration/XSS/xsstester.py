import requests
from bs4 import BeautifulSoup

# Define the target URL and headers
url = "https://sandbox-royal.securegateway.com/?search"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://sandbox-royal.securegateway.com/",
    "Origin": "https://sandbox-royal.securegateway.com",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Set cookies (update with valid PHPSESSID if necessary)
cookies = {
    "PHPSESSID": "78b7620ca5b5bea60ae1ab95bc19016f"
}

# Function to check for XSS in the response
def check_for_xss(response, payload):
    soup = BeautifulSoup(response.text, 'html.parser')
    if payload in response.text:
        print(f"XSS vulnerability found with payload: {payload}")
        return True
    return False

# Read the payloads from the txt file
def load_payloads(file_path):
    with open(file_path, 'r') as file:
        payloads = file.readlines()
    # Remove newline characters
    return [payload.strip() for payload in payloads]

# Main function to test XSS with payloads from a file
def test_xss_with_file(payload_file):
    payloads = load_payloads(payload_file)
    
    for payload in payloads:
        data = {'search': payload}
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        
        if check_for_xss(response, payload):
            print(f"Potential XSS detected with payload: {payload}")
        else:
            print(f"No XSS detected for payload: {payload}")

# Path to the file containing the payloads
payload_file = "xss_payloads.txt"

# Start the testing
test_xss_with_file(payload_file)
