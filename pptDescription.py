from pptx import Presentation
from GeminiAPI import print_file_description_and_key_findings
def process_PPT(file_path):
    prs = Presentation(file_path)
    slides_text = []
    for idx, slide in enumerate(prs.slides, start=1):
        text_list = []
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text and shape.text.strip():
                text_list.append(shape.text.strip())
        slide_text = "\n".join(text_list).strip()
        slides_text.append({"slide_index": idx, "text": slide_text})

    prompt=f"""
    Summarize the PPT file with the following text in about 30 words along with a suitable title:
    {slides_text}"""

    print_file_description_and_key_findings(prompt)