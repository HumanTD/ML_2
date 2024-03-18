import json
import PyPDF2
import textract
import re
import nltk
import requests

# Download NLTK punkt tokenizer
nltk.download('punkt')
results = []

# Retrieve JSON data from the URL
url = "https://a856-136-233-9-98.ngrok-free.app/?location=india"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print("Error:", response.status_code)
    exit()  # Exit the script if there's an error retrieving JSON data

# Open and extract text from the PDF
filename = r"D:\Users\Administrator\OneDrive - vit.ac.in\Desktop\Resume.pdf"
try:
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    num_pages = len(pdfReader.pages)

    text = ""
    for count in range(num_pages):
        pageObj = pdfReader.pages[count]
        text += pageObj.extract_text()

    # If text extraction failed, use alternative method
    if not text:
        text = textract.process('http://bit.ly/epo_keyword_extraction_document', method='tesseract', language='eng')
except Exception as e:
    print("Error processing PDF:", e)
    text = ""  # Reset text to empty string

# Specific keywords to identify for skills for different job roles
skills_keywords = {
    'Machine Learning': ['Machine Learning', 'Deep Learning', 'Python', 'TensorFlow', 'PyTorch', 'Natural Language Processing', 'Computer Vision'],
    'Software Developer': ['Java', 'JavaScript', 'HTML', 'CSS', 'ReactJS', 'Node.js', 'SQL', 'RESTful APIs'],
    'Data Analyst': ['SQL', 'Data Analysis', 'Statistics', 'Data Visualization', 'Python', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn'],
    'Product Manager': ['Product Management', 'Agile', 'Scrum', 'User Experience Design', 'Market Research', 'Product Strategy'],
    'DevOps Engineer': ['Linux', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'Jenkins', 'CI/CD'],
    'Cybersecurity Analyst': ['Cybersecurity', 'Network Security', 'Penetration Testing', 'Security Operations', 'Firewalls', 'Encryption'],
    'Full Stack Developer': ['JavaScript', 'HTML', 'CSS', 'ReactJS', 'Node.js', 'Python', 'Django', 'RESTful APIs', 'MongoDB', 'SQL']
}

# Find specific keywords in the text for each job role
skills_found = {role: [word for word in keywords if re.search(r'\b' + re.escape(word) + r'\b', text)] for role, keywords in skills_keywords.items()}

# Calculate match rate for each role
match_rates = {role: len(found_words) / len(skills_keywords[role]) * 100 if len(skills_keywords[role]) > 0 else 0 for role, found_words in skills_found.items()}

# Initialize variables to store the details of the company with the highest match rate
best_company_name = ""
best_title = ""
best_match_role = ""
best_match_rate = 0

# Iterate through each company's data
for company_data in data:
    company_name = company_data.get("name", "")  # Extract the company name from the dictionary
    title = company_data.get("title", "")  # Extract the job title

    # Iterate through each role and its keywords
    for role, keywords in skills_found.items():
        # Check if the role is found in the title
        if role.lower() in title.lower():
            # If there is a match, calculate the match rate for the role
            match_rate = match_rates.get(role, 0)
            print(match_rate)

            # If the match rate is higher than the current highest match rate, update the best match details
            if match_rate > best_match_rate:
                best_company_name = company_name
                best_title = title
                best_match_role = role
                best_match_rate = match_rate

# Append the details of the company with the highest match rate to the results list
results.append({
    "company": best_company_name,
    "title": best_title,
    "best_match_role": best_match_role,
    "match_rate": best_match_rate
})

# Save the dictionaries to a JSON file
output_data = {'results': results}
with open('skills.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=2)

print('JSON data saved to skills.json')
