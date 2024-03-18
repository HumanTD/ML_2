import PyPDF2
import openai

# Replace with your OpenAI API key
openai.api_key = "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"

def extract_text_from_pdf(pdf_path):
  try:
    with open(pdf_path, 'rb') as pdf_file:
      pdf_reader = PyPDF2.PdfReader(pdf_file)
      pages = pdf_reader.pages
      text = ""
      for page in pages:
        text += page.extract_text()
      return text
  except FileNotFoundError:
    print("Error: PDF file not found.")
    return None
  except Exception as e:
    print(f"An error occurred during PDF processing: {e}")
    return None

def answer_question_with_llm(question, text):
  try:
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Here is a document:\n{text}\n\nQuestion: {question}\n\nAnswer:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()
  except Exception as e:
    print(f"An error occurred during LLM processing: {e}")
    return None

# Specify the path to your PDF file
pdf_path = r"D:\Users\Administrator\OneDrive - vit.ac.in\Desktop\KashishDhokaCV_vit.pdf"

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_path)

if extracted_text:
  # Ask a question about the PDF content
  question = input("Ask a question about the document: ")

  # Answer the question using the LLM
  answer = answer_question_with_llm(question, extracted_text)

  if answer:
    print(f"Answer: {answer}")
  else:
    print("Failed to generate an answer.")
else:
  print("Failed to extract text from the PDF.")
