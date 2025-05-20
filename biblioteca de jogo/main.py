import streamlit as st
from PIL import Image
import os
import json

USERS_FILE = "users.json"

# --- Funções para manipular usuários ---
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- Setup ---
st.set_page_config(page_title="Game Rental Manager", layout="wide")

# --- Controle de login e registro ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None


# --- Menu para escolher Login ou Registro ---
menu = st.sidebar.selectbox("Menu", ["Login", "Criar Conta"])


if not st.session_state.logged_in:

    if menu == "Login":
        st.title("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            users = load_users()
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.role = users[username]["role"]
                st.rerun()
            else:
                st.error("Incorrect username or password.")
        st.stop()

    elif menu == "Criar Conta":
        st.title("📝 Criar Conta")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirmar Password", type="password")
        create_button = st.button("Criar Conta")

        if create_button:
            users = load_users()
            if not new_username or not new_password:
                st.error("Username e Password são obrigatórios.")
            elif new_password != confirm_password:
                st.error("As senhas não coincidem.")
            elif new_username in users:
                st.error("Usuário já existe. Escolha outro username.")
            else:
                users[new_username] = {"password": new_password, "role": "user"}
                save_users(users)
                st.success("Conta criada com sucesso! Agora faça login.")
                st.rerun()

else:
    # --- Logout ---
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

    # --- Saudação e info do usuário logado ---
    st.sidebar.markdown(f"👤 Usuário: **{st.session_state.user}**")
    st.sidebar.markdown(f"🛡️ Papel: **{st.session_state.role}**")

    # --- Language Selector ---
    language_map = {
        " Português": "Português",
        " English": "English",
        " Español": "Spanish",
        " Deutsch": "German",
        " Français": "French",
        " 中文": "Chinese",
        " 日本語": "Japanese",
        " Русский": "Russian",
        " العربية": "Arabic",
    }

    selected_label = st.sidebar.selectbox("🌐 Escolha o idioma", list(language_map.keys()))
    lang = language_map[selected_label]

    # --- Translation Dictionary ---
    TEXTS = {
        "Português": {
            "criar_conta": "Criar Conta",
            "login": "Login",
            "title": "🎮 Gestão de Aluguel de Jogos",
            "form_title": "📋 Formulário de Aluguel",
            "select_game": "Selecione um Jogo",
            "name": "Nome completo",
            "email": "Email",
            "phone": "Contacto",
            "phone_error1": "O contacto deve conter entre 9 a 15 dígitos.",
            "phone_error2": "O contacto deve ter entre 9 e 15 dígitos.",
            "days": "Número de dias para alugar",
            "submit": "Enviar Aluguel",
            "success": "Aluguel registado para",
            "error": "Por favor preencha todos os campos obrigatórios.",
            "recent": "🕹️ Jogos Recentemente Alugados",
            "rented_msg": "{} alugou {} por {} dia(s)",
        },
        "English": {
            "criar_conta": "Create Account",
            "login": "Login",
            "title": "🎮 Game Rental Manager",
            "form_title": "📋 Rental Form",
            "select_game": "Select a Game",
            "name": "Full Name",
            "email": "Email",
            "phone": "Phone Number",
            "phone_error1": "Phone number must contain between 9 and 15 digits.",
            "phone_error2": "Phone number must be between 9 and 15 digits.",
            "days": "Number of Days to Rent",
            "submit": "Submit Rental",
            "success": "Rental recorded for",
            "error": "Please fill in all required fields.",
            "recent": "🕹️ Recently Rented Games",
            "rented_msg": "{} rented {} for {} day(s)",
        },
        "Spanish": {
            "criar_conta": "Crear Cuenta",
            "login": "Iniciar Sesión",
            "title": "🎮 Gestor de Alquiler de Juegos",
            "form_title": "📋 Formulario de Alquiler",
            "select_game": "Selecciona un Juego",
            "name": "Nombre completo",
            "email": "Correo electrónico",
            "phone": "Número de contacto",
            "phone_error1": "El número de contacto debe contener entre 9 y 15 dígitos.",
            "phone_error2": "El número de contacto debe tener entre 9 y 15 dígitos.",
            "days": "Número de días para alquilar",
            "submit": "Enviar Alquiler",
            "success": "Alquiler registrado para",
            "error": "Por favor, completa todos los campos obligatorios.",
            "recent": "🕹️ Juegos Alquilados Recientemente",
            "rented_msg": "{} alquiló {} por {} día(s)",
        },
        "German": {
            "criar_conta": "Benutzerkonto erstellen",
            "login": "Anmelden",
            "title": "🎮 Spielverleih-Manager",
            "form_title": "📋 Verleihformular",
            "select_game": "Wählen Sie ein Spiel",
            "name": "Vollständiger Name",
            "email": "E-Mail",
            "phone": "Telefonnummer",
            "phone_error1": "Die Telefonnummer muss zwischen 9 und 15 Ziffern enthalten.",
            "phone_error2": "Die Telefonnummer muss zwischen 9 und 15 Ziffern liegen.",
            "days": "Anzahl der Tage zur Miete",
            "submit": "Verleih einreichen",
            "success": "Verleih registriert für",
            "error": "Bitte füllen Sie alle erforderlichen Felder aus.",
            "recent": "🕹️ Kürzlich vermietete Spiele",
            "rented_msg": "{} mietete {} für {} Tag(e)",
        },
        "French": {
            "criar_conta": "Créer un Compte",
            "login": "Connexion",
            "title": "🎮 Gestion de Location de Jeux",
            "form_title": "📋 Formulaire de Location",
            "select_game": "Sélectionnez un Jeu",
            "name": "Nom complet",
            "email": "E-mail",
            "phone": "Numéro de téléphone",
            "phone_error1": "Le numéro de téléphone doit contenir entre 9 et 15 chiffres.",
            "phone_error2": "Le numéro de téléphone doit être entre 9 et 15 chiffres.",
            "days": "Nombre de jours à louer",
            "submit": "Soumettre la Location",
            "success": "Location enregistrée pour",
            "error": "Veuillez remplir tous les champs obligatoires.",
            "recent": "🕹️ Jeux Récemment Loués",
            "rented_msg": "{} a loué {} pour {} jour(s)",
        },
        "Chinese": {
            "criar_conta": "创建账户",
            "login": "登录",
            "title": "🎮 游戏租赁管理器",
            "form_title": "📋 租赁表格",
            "select_game": "选择一个游戏",
            "name": "全名",
            "email": "电子邮件",
            "phone": "电话号码",
            "phone_error1": "电话号码必须包含9到15位数字。",
            "phone_error2": "电话号码必须在9到15位之间。",
            "days": "租赁天数",
            "submit": "提交租赁",
            "success": "租赁记录为",
            "error": "请填写所有必填字段。",
            "recent": "🕹️ 最近租赁的游戏",
            "rented_msg": "{} 租赁了 {} 为期 {} 天",
        },
        "Japanese": {
            "criar_conta": "アカウントを作成",
            "login": "ログイン",
            "title": "🎮 ゲームレンタルマネージャー",
            "form_title": "📋 レンタルフォーム",
            "select_game": "ゲームを選択",
            "name": "フルネーム",
            "email": "メール",
            "phone": "電話番号",
            "phone_error1": "電話番号は9〜15桁の数字でなければなりません。",
            "phone_error2": "電話番号は9〜15桁でなければなりません。",
            "days": "レンタル日数",
            "submit": "レンタルを提出",
            "success": "レンタルが記録されました",
            "error": "必須フィールドにすべて入力してください。",
            "recent": "🕹️ 最近レンタルされたゲーム",
            "rented_msg": "{} が {} を {} 日間レンタルしました",
        },
        "Russian": {
            "criar_conta": "Создать аккаунт",
            "login": "Войти",
            "title": "🎮 Менеджер аренды игр",
            "form_title": "📋 Форма аренды",
            "select_game": "Выберите игру",
            "name": "Полное имя",
            "email": "Электронная почта",
            "phone": "Номер телефона",
            "phone_error1": "Номер телефона должен содержать от 9 до 15 цифр.",
            "phone_error2": "Номер телефона должен быть от 9 до 15 цифр.",
            "days": "Количество дней аренды",
            "submit": "Отправить аренду",
            "success": "Аренда зарегистрирована для",
            "error": "Пожалуйста, заполните все обязательные поля.",
            "recent": "🕹️ Недавно арендованные игры",
            "rented_msg": "{} арендовал {} на {} день(ей)",
        },
        "Arabic": {
            "criar_conta": "إنشاء حساب",
            "login": "تسجيل الدخول",
            "title": "🎮 مدير تأجير الألعاب",
            "form_title": "📋 نموذج الإيجار",
            "select_game": "اختر لعبة",
            "name": "الاسم الكامل",
            "email": "البريد الإلكتروني",
            "phone": "رقم الهاتف",
            "phone_error1": "يجب أن يحتوي رقم الهاتف على 9 إلى 15 رقمًا.",
            "phone_error2": "يجب أن يكون رقم الهاتف بين 9 و 15 رقمًا.",
            "days": "عدد الأيام للإيجار",
            "submit": "إرسال الإيجار",
            "success": "تم تسجيل الإيجار لـ",
            "error": "يرجى ملء جميع الحقول المطلوبة.",
            "recent": "🕹️ الألعاب المستأجرة مؤخرًا",
            "rented_msg": "{} استأجر {} لمدة {} يوم(أيام)",
        },
    }

    T = TEXTS[lang]

    # --- Lista dos jogos com preços ---
    most_played_games = [
        {"title": "God of War", "filename": "god_of_war.jpg", "price": 5.00},
        {"title": "Grand Theft Auto VI", "filename": "gtavi.jpg", "price": 6.50},
        {"title": "Counter Strike 2 (prime)", "filename": "cs2.jpg", "price": 4.75},
        {"title": "EA SPORTS FC™ 25 Ultimate Edition", "filename": "ea_25_ult.jpg", "price": 7.20},
        {"title": "EA SPORTS FC™ 25 Standart Edition", "filename": "ea_25_stand.jpg", "price": 6.00},
    ]

    # --- Histórico de aluguéis na sessão ---
    if "recent_rentals" not in st.session_state:
        st.session_state.recent_rentals = []

    # --- Título ---
    st.title(T["title"])

    # --- Barra de pesquisa (atualiza automaticamente a cada letra) ---
    search_query = st.text_input("🔎 Pesquisar jogo", value="", key="search_bar")

    # Filtra os jogos conforme a pesquisa (case-insensitive)
    if search_query:
        filtered_games = [game for game in most_played_games if search_query.lower() in game["title"].lower()]
    else:
        filtered_games = most_played_games

    # --- Defina as abas principais ---
    aba = st.sidebar.radio("Navegação", ["Biblioteca", "Alugar Jogo"])

    # --- Exibe todos os jogos como uma biblioteca em várias colunas ---
    if aba == "Biblioteca":
        st.subheader("📚 Biblioteca de Jogos")
        cols = st.columns(3)  # 3 colunas

        for idx, game in enumerate(filtered_games):
            with cols[idx % 3]:
                image_path = os.path.join("images", game["filename"])
                if os.path.exists(image_path):
                    st.image(Image.open(image_path), width=200, caption=game["title"])
                else:
                    st.warning(f"Imagem não encontrada: {game['filename']}")
                st.markdown(f"**Preço por dia:** ${game['price']:.2f}")

                # Botão para adquirir/alugar o jogo
                if st.button(f"🎮 Adquirir '{game['title']}'", key=f"acquire_{idx}"):
                    st.session_state.selected_game = game
                    st.session_state.show_rent_form = True
                    st.session_state.aba = "Alugar Jogo"
                    st.rerun()

    # --- Formulário de aluguel em outra aba ---
    if aba == "Alugar Jogo" or st.session_state.get("aba") == "Alugar Jogo":
        st.subheader(T["form_title"])
        selected_game = st.session_state.get("selected_game", None)
        if selected_game:
            st.markdown(f"**{T['select_game']}:** {selected_game['title']}")
            name = st.text_input(T["name"])
            email = st.text_input(T["email"])
            phone = st.text_input(T["phone"])
            days = st.number_input(T["days"], min_value=1, max_value=30, value=1)
            submit_rent = st.button(T["submit"])

            if submit_rent:
                if not name or not email or not phone:
                    st.error(T["error"])
                elif not phone.isdigit() or not (9 <= len(phone) <= 15):
                    st.error(T["phone_error2"])
                else:
                    st.session_state.recent_rentals.append({
                        "name": name,
                        "game": selected_game["title"],
                        "days": days
                    })
                    st.success(f"{T['success']} {name}!")
                    st.session_state.show_rent_form = False
                    st.session_state.aba = "Biblioteca"
                    st.rerun()
