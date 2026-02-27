import os
import google.generativeai as genai
from dotenv import load_dotenv
from flaskblog import app, db
from flaskblog.models import User, Post

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_ai_post():
    """Funkcja łącząca się z modelem AI w celu wygenerowania tekstu."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
    Napisz krótki post na bloga z dowolnym przepisem kulinarnym. Pisz krótko i zwięźle sam przepis, bez zwrotów do czytelników, profesjonalnie i sucho.
    Zwróć wynik dokładnie w takim formacie:
    W pierwszej linijce sam tytuł.
    Od drugiej linijki treść posta.
    """
    
    response = model.generate_content(prompt)
    
    lines = response.text.split('\n', 1)
    title = lines[0].strip().replace('**', '') # Usuwamy ewentualne pogrubienia z tytułu
    content = lines[1].strip() if len(lines) > 1 else "Brak treści."
    
    return title, content

def save_post_to_db(title, content):
    
    app.app_context().push()
    bot_user = User.query.filter_by(email='cookbot@mojadomena.pl').first()

    if not bot_user:
        print("Błąd: Nie znaleziono konta bota w bazie danych!")
        return

    new_post = Post(title=title, content=content, author=bot_user)

    db.session.add(new_post)
    db.session.commit()
    print(f"Sukces! Dodano nowy post: {title}")

if __name__ == '__main__':
    print("Rozpoczynam pracę AI...")
    post_title, post_content = generate_ai_post()
    save_post_to_db(post_title, post_content)