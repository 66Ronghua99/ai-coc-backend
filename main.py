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

def main():
    load_dotenv()
    
    # Initialize game
    game = CoCGame()
    
    # Load module
    module_path = os.path.join("docs", "scary_fall.docx")
    module_texts = load_module_from_doc(module_path)
    game.load_module(module_texts)
    
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