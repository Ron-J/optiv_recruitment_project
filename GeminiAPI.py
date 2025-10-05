import os
import google.generativeai as genai

def print_file_description_and_key_findings(prompt: str) -> str:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')

    response1 = model.generate_content(prompt)

    #print("\nFile Description")
    #print(response.text)

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    

    prompt = f"""
    Analyze the following file description and extract the key findings. The findings should summarize the system's purpose, functionality, advantages, and potential vulnerabilities. Follow the format of the examples provided.
    ---
    **Example 1:**

    **File Description:**
    Access Card Reader

    A person is holding an access card against a card reader mounted near a door labeled "211 IDF/Electrical." The card reader has a light indicator.

    **Key Findings:**
    - Digital access control system using ID/employee cards.
    - Automates entry tracking by time-stamping when the card is swiped.
    - Dependent on card validity and system integrity (e.g., cards can be lost or borrowed).

    ---
    **Example 2:**

    **File Description:**
    Biometric Attendance/Access System

    A wall-mounted electronic biometric device with fingerprint scanning, keypad, and display screen showing time.

    **Key Findings:**
    - Uses biometric authentication (fingerprint) for high security.
    - Eliminates risks of proxy entry or shared access (unlike cards or logbooks).
    - Provides accurate, automated attendance and access logs.
    - Suitable for organizations seeking reliable and tamper-proof entry systems.

    ---
    **Example 3:**

    **File Description:**
    Visitors Logbook

    A paper-based visitor logbook where individuals manually write their name, reason for visit, time in/out, and provide a signature. Two entries are already filled in.

    **Key Findings:**
    - Manual entry system, dependent on handwriting.
    - Prone to errors, illegible writing, and falsification.
    - No automatic time tracking—relies on honesty and accuracy of the visitor.

    ---
    **New Request:**

    **File Description:**
    {response1.text}

    **Key Findings:**
    """
    # Generate content using the model
    response2 = model.generate_content(prompt)
        
    # Clean up the response text to ensure consistent formatting
    '''findings_list = [
        line.strip().lstrip('- ').strip() 
        for line in response.text.strip().split('\n') 
        if line.strip()
    ]
    print("\n\nKey Findings: ")
    print("\n".join(f"- {finding}" for finding in findings_list))'''
    return response1.text+"\n\n"+response2.text

