import pandas as pd
import re
from GeminiAPI import print_file_description_and_key_findings
import os
import warnings
from fileCleaning import clean_excel
warnings.filterwarnings('ignore', category=FutureWarning, message='DataFrame.applymap has been deprecated')
PII_PATTERNS = {
    "SSN": r'\b\d{3}-\d{2}-\d{4}\b',  # Simple Social Security Number pattern
    "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "IP_ADDRESS": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', 
    # Masking for common placeholders or sensitive client names/IDs
    "CLIENT_NAME": r'\b(Client|Organization|Company)\s+[A-Z]\w+\b', 
}
def mask_pii_in_text(text: str) -> str:
    """Applies regex patterns to mask sensitive information within a string."""
    if not isinstance(text, str):
        text = str(text) if pd.notna(text) else ""
    masked_text = text
    for pii_type, pattern in PII_PATTERNS.items():
        masked_text = re.sub(pattern, f"[{pii_type}_MASKED]", masked_text, flags=re.IGNORECASE)
    return masked_text
def extract_and_cleanse_excel(file_path: str) -> str:
    """
    Reads an Excel file, cleanses all cell contents, and concatenates 
    the cleansed data into a single string for analysis.
    """
    try:
        xls = pd.ExcelFile(file_path)
        all_cleansed_text = []
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, engine='openpyxl')
            df_cleansed = df.map(mask_pii_in_text)
            sheet_text = f"\n--- Sheet: {sheet_name} ---\n"
            sheet_text += df_cleansed.to_string(index=False, header=True)
            all_cleansed_text.append(sheet_text)
        return "\n\n".join(all_cleansed_text)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
    except Exception as e:
        print(f"Error processing Excel file {file_path}: {e}")
        return ""
def process_EXCEL(file_path: str):
    clean_excel(file_path)
    """
    Main function to process Excel files, cleanse, extract text, 
    and call the Gemini API for description and findings.
    """
    cleansed_content = extract_and_cleanse_excel(file_path)
    if cleansed_content:
        prompt = f"""
        Analyze the following cleansed spreadsheet data (Excel file). Generate a descriptive 
        title and a file caption of about 30 words that summarizes the data's content, 
        focusing on the security/IT-related context (e.g., Firewall rules, User Access Log, 
        Token Issuance, etc.).
        Cleansed Spreadsheet Content:
        ---
        {cleansed_content}
        """
        return print_file_description_and_key_findings(prompt)
    else:
        print(f"Could not generate description for {os.path.basename(file_path)} due to processing error.")