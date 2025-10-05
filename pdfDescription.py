import pypdf
import re
import pandas as pd
from GeminiAPI import print_file_description_and_key_findings
from fileCleaning import clean_pdf
def extract_and_cleanse_pdf(file_path):
    """
    Extracts text from a PDF, cleanses it by replacing placeholders, and returns the cleaned text.
    """
    cleaned_text = ""
    try:
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    # Replace specific placeholders with generic terms for cleansing
                    text = re.sub(r"\[Organization Name\]", "[Client]", text, flags=re.IGNORECASE)
                    text = re.sub(r"\[IT Service Desk\]", "[Service Desk]", text, flags=re.IGNORECASE)
                    text = re.sub(r"\[Information Security Manager\]", "[Security Manager]", text, flags=re.IGNORECASE)
                    cleaned_text += text
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    return cleaned_text

def find_key_findings(text):
    """
    Analyzes the text for key security-related findings and returns them as a list.
    """
    findings = []
    
    # 1. Privileged Access Management
    if re.search(r"privileged access rights", text, re.IGNORECASE):
        findings.append("The document details a process for managing privileged access rights that is more rigorous than for standard users.")
        findings.append("It specifies that users needing privileged access must have a separate, dedicated account.")
        findings.append("The default admin account's password should never be issued.")
    
    # 2. User Deregistration
    if re.search(r"deregistration", text, re.IGNORECASE):
        findings.append("When employees leave, their accounts are disabled rather than deleted to retain information and prevent unauthorized access.")
        findings.append("Accounts are to be disabled in order of importance, with the most critical systems (e.g., Finance) being a priority.")
        findings.append("Any physical authentication tokens must be retrieved during the termination process.")
        
    # 3. Access Reviews
    if re.search(r"user access review", text, re.IGNORECASE):
        findings.append("A user access review is required every six months to ensure that access is limited to authorized personnel.")
        findings.append("The review process is used to identify leavers, accounts with excessive access, and generic or shared accounts.")
        
    # 4. Password & Authentication
    if re.search(r"password", text, re.IGNORECASE):
        findings.append("The initial password set by the [Service Desk] is strong and expires upon first logon, requiring the user to create a new one.")
        findings.append("The initial password should be communicated to the user by telephone or another secure method, not left as a message.")
    
    return " ".join(findings)

def create_findings_table(file_name, file_type, file_description, key_findings):
    """
    Creates a pandas DataFrame to represent the findings table.
    """
    data = {
        'File Name': [file_name],
        'File Type': [file_type],
        'File Description': [file_description],
        'Key Findings': [key_findings]
    }
    df = pd.DataFrame(data)
    return df

def save_findings_to_file(dataframe, filename="findings_output.txt"):
    """
    Saves the pandas DataFrame to a text file.
    """
    with open(filename, "w") as f:
        f.write("--- Final Output for PowerPoint Table ---\n")
        f.write(dataframe.to_string(index=False))

def process_PDF(file_path):
    clean_pdf(file_path)
    # Step 1: Extract and Cleanse
    cleansed_text = extract_and_cleanse_pdf(file_path)
    
    if cleansed_text:
        # Step 2: Interpret and find key findings
        description = "This document outlines an organization's User Access Management policies and procedures, including user registration, access adjustment, and de-registration."
        findings = find_key_findings(cleansed_text)
        
        # Step 3: Create the table
        findings_df = create_findings_table(
            "File_012",
            ".pdf",
            description,
            findings
        )
        
        # Step 4: Save the output to a file
        #save_findings_to_file(findings_df)
        
        #print("Output saved to findings_output.txt. Please open this file in your project folder to see the complete table.")
        prompt=f"""Based on the following text detected from a PDF file generate a title and file description of about 30 words.
        Detected Text:
        {cleansed_text}
        """
        return print_file_description_and_key_findings(prompt)