import os
from google import genai
from google.genai.types import HttpOptions
from dotenv import load_dotenv
from flaskblog import app, db
from flaskblog.models import User, Post

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

adres_proxy = 'http://uozcazcy:89v4wnjqsqs8@23.95.150.145:6114'

http_options = HttpOptions(client_args={"proxy": adres_proxy})
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"), 
    http_options=http_options
)

def generate_ai_post():
    prompt = """
    Napisz krótki post na bloga z dowolnym przepisem kulinarnym. Pisz krótko i zwięźle sam przepis, bez zwrotów do czytelników, profesjonalnie i sucho.
    Zwróć wynik dokładnie w takim formacie:
    W pierwszej linijce sam tytuł.
    Od drugiej linijki treść posta.
    """
    
    response = client.models.generate_content(
	model='gemini-2.5-flash',
	contents=prompt
    )
    
    lines = response.text.split('\n', 1)
    title = lines[0].strip().replace('*', '')
    content = lines[1].strip().replace('*', '')  if len(lines) > 1 else "Brak treści."
    
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
