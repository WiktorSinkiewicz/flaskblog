import os
import random
import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from flaskblog import app, db
from flaskblog.models import User, Post

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_ai_post():
    """Funkcja łącząca się z modelem AI w celu wygenerowania tekstu."""
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    
    now = datetime.datetime.now()
    months_context = {
        1: "styczeń (zima, dania noworoczne, rozgrzewające)", 
        2: "luty (zima, karnawał, tłusty czwartek)", 
        3: "marzec (przedwiośnie, lekkie dania)",
        4: "kwiecień (wiosna, Wielkanoc, nowalijki)", 
        5: "maj (wiosna, szparagi, sezon grillowy)", 
        6: "czerwiec (lato, truskawki, chłodniki)",
        7: "lipiec (lato, wakacje, owoce leśne)", 
        8: "sierpień (lato, upały, pomidory, cukinia)", 
        9: "wrzesień (jesień, grzyby, śliwki)",
        10: "październik (jesień, dynie, jabłka, potrawy sycące)", 
        11: "listopad (późna jesień, dania jednogarnkowe, pieczenie)", 
        12: "grudzień (zima, Boże Narodzenie, korzenne przyprawy)"
    }
    current_context = months_context.get(now.month, "dowolny sezon")
    
    regions = [
        "Włochy", "Francja", "Hiszpania", "Meksyk", "Japonia",
        "Tajlandia", "Indie", "Grecja", "Polska", "Bliski Wschód",
        "Korea Południowa", "Wietnam", "Maroko", "Gruzja",
        "Skandynawia", "Peru", "Chiny (Syczuan)", "Liban"
    ]
    
    meal_types = [
        "zupa", "danie główne mięsne", "danie główne wegetariańskie", 
        "danie rybne / owoce morza", "przekąska / tapas", "deser", 
        "sałatka", "danie z makaronem", "wypiek (chleb, tarta)"
    ]
    
    chosen_region = random.choice(regions)
    chosen_meal_type = random.choice(meal_types)
    
    prompt = f"""
    Napisz krótki post na bloga z przepisem kulinarnym. 
    Wymagania dotyczące przepisu:
    - Region kulinarny / styl: {chosen_region}.
    - Rodzaj dania: {chosen_meal_type}.
    - Kontekst czasowy i sezonowy: {current_context}. Bezwzględnie dopasuj użyte składniki do tego okresu.
    
    Wykorzystaj powyższe wytyczne, aby wymyślić unikalny, rzadziej spotykany przepis. Unikaj najbardziej banalnych, oczywistych klasyków.
    
    Pisz krótko i zwięźle sam przepis, bez zwrotów do czytelników, profesjonalnie i sucho.
    Zwróć wynik dokładnie w takim formacie:
    W pierwszej linijce sam tytuł.
    Od drugiej linijki treść posta.
    """
    
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.85,
        )
    )
    
    lines = response.text.split('\n', 1)
    title = lines[0].strip().replace('**', '')
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