import os
from dotenv import load_dotenv
from src.game import CoCGame
from docx import Document
import PyPDF2  # Added import for PDF handling

def load_module_from_doc(doc_path: str) -> list:
    """Load module text from a .doc file."""
    doc = Document(doc_path)
    texts = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            texts.append(paragraph.text)
    return texts

def load_rules_from_pdf(pdf_path: str) -> list:
    """Load rules text from a .pdf file."""
    texts = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text.strip():
                # Split by lines and add non-empty lines
                for line in text.split('\n'):
                    if line.strip():
                        texts.append(line.strip())
    return texts

def main():
    load_dotenv()
    
    # Initialize game
    game = CoCGame()
    
    # Load module
    module_path = os.path.join("docs", "scary_fall.docx")
    rules_path = os.path.join("docs", "COC_rule.pdf")
    module_texts = load_module_from_doc(module_path)
    rules_texts = load_rules_from_pdf(rules_path)
    game.load_module(module_texts)
    game.load_rules(rules_texts)
    
    print("Welcome to the Call of Cthulhu game!")
    print("Type 'quit' to exit the game.")
    
    while True:
        player_input = input("\nYou: ").strip()
        if player_input.lower() == 'quit':
            break
            
        response = game.process_player_input(player_input)
        print(f"\nGame Master: {response}")

if __name__ == "__main__":
    main()