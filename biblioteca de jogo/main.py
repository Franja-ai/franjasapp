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


# --- Dicionário de idiomas e textos ---
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
    " Polski": "Polish",
}

TEXTS = {
    "Português": {
        "menu": "Menu",
        "login": "Login",
        "criar_conta": "Criar Conta",
        "user": "Usuário",
        "role": "Papel",
        "choose_language": "Escolha o idioma",
        "navigation": "Navegação",
        "biblioteca": "Biblioteca",
        "alugar_jogo": "Alugar Jogo",
        "title": "🎮 Gestão de Aluguer de Jogos",
        "form_title": "📋 Formulário de Aluguer",
        "select_game": "Selecione um Jogo",
        "name": "Nome completo",
        "email": "Email",
        "phone": "Contacto",
        "phone_error1": "O contacto deve conter entre 9 a 15 dígitos.",
        "phone_error2": "O contacto deve ter entre 9 e 15 dígitos.",
        "days": "Número de dias para alugar",
        "submit": "Enviar Aluguer",
        "success": "Aluguer registado para",
        "error": "Por favor preencha todos os campos obrigatórios.",
        "recent": "🕹️ Jogos Recentemente Alugados",
        "rented_msg": "{} alugou {} por {} dia(s)",
    },
    "English": {
        "menu": "Menu",
        "login": "Login",
        "criar_conta": "Create Account",
        "user": "User",
        "role": "Role",
        "choose_language": "Choose language",
        "navigation": "Navigation",
        "biblioteca": "Library",
        "alugar_jogo": "Rent Game",
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
        "menu": "Menú",
        "login": "Iniciar Sesión",
        "criar_conta": "Crear Cuenta",
        "user": "Usuario",
        "role": "Rol",
        "choose_language": "Elige idioma",
        "navigation": "Navegación",
        "biblioteca": "Biblioteca",
        "alugar_jogo": "Alquilar Juego",
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
        "success": "Aluguel registrado para",
        "error": "Por favor, completa todos los campos obligatorios.",
        "recent": "🕹️ Juegos Alquilados Recientemente",
        "rented_msg": "{} alquiló {} por {} día(s)",
    },
    "German": {
        "menu": "Menü",
        "login": "Anmelden",
        "criar_conta": "Konto erstellen",
        "user": "Benutzer",
        "role": "Rolle",
        "choose_language": "Sprache wählen",
        "navigation": "Navigation",
        "biblioteca": "Bibliothek",
        "alugar_jogo": "Spiel mieten",
        "title": "🎮 Spielverleih-Manager",
        "form_title": "📋 Verleihformular",
        "select_game": "Spiel auswählen",
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
        "menu": "Menu",
        "login": "Connexion",
        "criar_conta": "Créer un compte",
        "user": "Utilisateur",
        "role": "Rôle",
        "choose_language": "Choisir la langue",
        "navigation": "Navigation",
        "biblioteca": "Bibliothèque",
        "alugar_jogo": "Louer un jeu",
        "title": "🎮 Gestion de Location de Jeux",
        "form_title": "📋 Formulaire de Location",
        "select_game": "Sélectionnez un jeu",
        "name": "Nom complet",
        "email": "E-mail",
        "phone": "Numéro de téléphone",
        "phone_error1": "Le numéro de téléphone doit contenir entre 9 et 15 chiffres.",
        "phone_error2": "Le numéro de téléphone doit être entre 9 et 15 chiffres.",
        "days": "Nombre de jours à louer",
        "submit": "Soumettre la location",
        "success": "Location enregistrée pour",
        "error": "Veuillez remplir tous les champs obligatoires.",
        "recent": "🕹️ Jeux récemment loués",
        "rented_msg": "{} a loué {} pour {} jour(s)",
    },
    "Chinese": {
        "menu": "菜单",
        "login": "登录",
        "criar_conta": "创建账户",
        "user": "用户",
        "role": "角色",
        "choose_language": "选择语言",
        "navigation": "导航",
        "biblioteca": "游戏库",
        "alugar_jogo": "租赁游戏",
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
        "menu": "メニュー",
        "login": "ログイン",
        "criar_conta": "アカウントを作成",
        "user": "ユーザー",
        "role": "役割",
        "choose_language": "言語を選択",
        "navigation": "ナビゲーション",
        "biblioteca": "ライブラリ",
        "alugar_jogo": "ゲームをレンタル",
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
        "menu": "Меню",
        "login": "Войти",
        "criar_conta": "Создать аккаунт",
        "user": "Пользователь",
        "role": "Роль",
        "choose_language": "Выберите язык",
        "navigation": "Навигация",
        "biblioteca": "Библиотека",
        "alugar_jogo": "Арендовать игру",
        "title": "🎮 Менеджер аренды игр",
        "form_title": "📋 Форма аренды",
        "select_game": "Выберите игру",
        "name": "Полное имя",
        "email": "Электронная почта",
        "phone": "Номер телефона",
        "phone_error1": "Номер телефона должен содержать от 9 до 15 цифр.",
        "phone_error2": "Номер телефона должен быть от 9 до 15",
        "days": "Количество дней аренды",
        "submit": "Отправить аренду",
        "success": "Аренда зарегистрирована для",
        "error": "Пожалуйста, заполните все обязательные поля.",
        "recent": "🕹️ Недавно арендованные игры",
        "rented_msg": "{} арендовал {} на {} день(ей)",
    },
    "Arabic": {
        "menu": "القائمة",
        "login": "تسجيل الدخول",
        "criar_conta": "إنشاء حساب",
        "user": "المستخدم",
        "role": "الدور",
        "choose_language": "اختر اللغة",
        "navigation": "التنقل",
        "biblioteca": "المكتبة",
        "alugar_jogo": "استئجار لعبة",
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
    "Polish": {
        "menu": "Menu",
        "login": "Zaloguj się",
        "criar_conta": "Utwórz konto",
        "user": "Użytkownik",
        "role": "Rola",
        "choose_language": "Wybierz język",
        "navigation": "Nawigacja",
        "biblioteca": "Biblioteka",
        "alugar_jogo": "Wypożycz grę",
        "title": "🎮 Menedżer Wypożyczeń Gier",
        "form_title": "📋 Formularz Wypożyczenia",
        "select_game": "Wybierz grę",
        "name": "Pełne imię",
        "email": "E-mail",
        "phone": "Numer telefonu",
        "phone_error1": "Numer telefonu musi zawierać od 9 do 15 cyfr.",
        "phone_error2": "Numer telefonu musi mieć od 9 do 15 cyfr.",
        "days": "Liczba dni wypożyczenia",
        "submit": "Wyślij wypożyczenie",
        "success": "Wypożyczenie zarejestrowane dla",
        "error": "Proszę wypełnić wszystkie wymagane pola.",
        "recent": "🕹️ Ostatnio wypożyczone gry",
        "rented_msg": "{} wypożyczył {} na {} dzień(i)",
    },
}

# --- Seleção de idioma sempre visível ---
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = " Português"
selected_label = st.sidebar.selectbox(
    "🌐 Escolha o idioma",
    list(language_map.keys()),
    index=list(language_map.keys()).index(st.session_state.selected_lang),
    key="sidebar_language_select"
)
st.session_state.selected_lang = selected_label
lang = language_map[selected_label]
T = TEXTS[lang]

# --- Menu para escolher Login ou Registro ---
if not st.session_state.logged_in:
    menu = st.sidebar.selectbox(T["menu"], [T["login"], T["criar_conta"]], key="sidebar_auth_menu")

    if menu == T["login"]:
        st.title("🔐 " + T["login"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button(T["login"])

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

    elif menu == T["criar_conta"]:
        st.title("📝 " + T["criar_conta"])
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirmar Password", type="password")
        create_button = st.button(T["criar_conta"])

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
    # --- Botão de logout ---
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.aba = None
        st.session_state.selected_game = None
        st.rerun()

    # --- Saudação e info do usuário logado (agora traduzido) ---
    st.sidebar.markdown(f"👤 {T['user']}: **{st.session_state.user}**")
    st.sidebar.markdown(f"🛡️ {T['role']}: **{st.session_state.role}**")

    # --- Lista dos jogos com preços ---
    most_played_games = [
        {"title": "Grand Theft Auto VI", 
         "price": 6.50,
         "url": "https://gaming-cdn.com/images/products/2462/616x353/grand-theft-auto-vi-pc-jogo-rockstar-cover.jpg?v=1746543065"
         },
        {"title": "Counter Strike 2 (prime)", 
         "price": 4.75,
         "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg?t=1696498820"
         },
        {"title": "EA SPORTS FC™ 25 Ultimate Edition", 
         "price": 7.20,
         "url": "https://image.api.playstation.com/vulcan/ap/rnd/202407/1814/ad53de47262b4bd4bf41f1f62f7feb40095b7716e26a3d1c.jpg"
         },
        {"title": "EA SPORTS FC™ 25 Standart Edition",
         "price": 6.00,
         "url": "https://image.api.playstation.com/vulcan/ap/rnd/202503/2520/f9bf56d8e1489be01e98aaf5040a54ad4e7d7af183901f17.jpg"
        },
        {"title": "Call of Duty®: Modern Warfare® II", 
         "price": 5.50,
         "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1938090/header.jpg?t=1696498820"
         },
        {"title": "The Last of Us™ Part I", 
         "price": 8.00,
         "url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2254450/ss_3f4425df24a8bfe3aee98991da893c9d43413f38.1920x1080.jpg?t=1727477866"
        },
        {"title": "The Last of Us™ Part II",
         "price": 7.00,
         "url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2531310/94b5d8b3165a6fe592e406054b08a2dd24e2f848/capsule_616x353.jpg?t=1746152571"
         },
        {"title": "Cyberpunk 2077", 
         "price": 5.00,
         "url": "https://image.api.playstation.com/vulcan/ap/rnd/202311/2812/ae84720b553c4ce943e9c342621b60f198beda0dbf533e21.jpg"
         },
        {"title": "The Witcher 3: Wild Hunt", 
         "price": 4.00,
         "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/292030/header.jpg?t=1696498820"
         },
        {"title": "Minecraft",
         "price": 3.50,
         "url": "https://assets.nintendo.com/image/upload/f_auto/q_auto/dpr_1.5/c_scale,w_400/ncom/software/switch/70070000016597/0a33bcaba879403460afe2ff2aafaaefeede964e0fc11a430f71077867cc87f1"
         },
        {"title": "The Sims™ 4", 
         "price": 4.25,
         "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1222670/header.jpg?t=1696498820"
         },
        {"title": "among us",
         "price": 2.50,
         "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/945360/header.jpg?t=1696498820"
         },
        {"title": "Supermaket Simulator 2",
         "price": 3.00,
         "url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2670630/capsule_616x353.jpg?t=1747747913"
         },
        {"title": "Euro Truck Simulator 2",
         "price": 4.50,
         "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/227300/header.jpg?t=1696498820"
         },
        {"title": "GOd of War™ Ragnarök",
         "price": 7.50, 
         "url": "https://image.api.playstation.com/vulcan/ap/rnd/202503/2016/9c66234099a4c6dc39a12c4101746f7dc9d87babbca5efe4.jpg"
         },
        {"title": "Need for Speed™ Unbound", 
         "price": 6.25,
         "url": "https://gmedia.playstation.com/is/image/SIEPDC/Need-for-speed-unbound-listing-thumb-en-01-20sep22?$native$"
         },
        {"title": "Red Dead Redemption 2",
         "price": 5.75,
         "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/header.jpg?t=1696498820"
        },

    ]

    # --- Histórico de aluguéis na sessão ---
    if "recent_rentals" not in st.session_state:
        st.session_state.recent_rentals = []

    # --- Título ---
    st.title(T["title"])

    # --- Barra de pesquisa (atualiza automaticamente a cada letra) ---
    search_query = st.text_input(f"🔎 {T['select_game']}", value="", key="search_bar")

    # Filtra os jogos conforme a pesquisa (case-insensitive)
    if search_query:
        filtered_games = [game for game in most_played_games if search_query.lower() in game["title"].lower()]
    else:
        filtered_games = most_played_games

    # --- Exibe todos os jogos como uma biblioteca em várias colunas ---
    st.subheader(f"📚 {T['biblioteca']}")
    cols = st.columns(3)  # 3 colunas

    for idx, game in enumerate(filtered_games):
        with cols[idx % 3]:
            # Se houver URL, usa a imagem online, senão tenta local
            if "url" in game and game["url"]:
                st.image(game["url"], width=200, caption=game["title"])
            else:
                image_path = os.path.join("images", game.get("filename", ""))
                if os.path.exists(image_path):
                    st.image(Image.open(image_path), width=200, caption=game["title"])
                else:
                    st.warning(f"{T['error']} ({game.get('filename', '')})")
            st.markdown(f"**{T['days']}:** ${game['price']:.2f}")
            # Botão para alugar jogo
            if st.button(T["alugar_jogo"], key=f"rent_{idx}"):
                st.session_state.aba = T["alugar_jogo"]
                st.session_state.selected_game = game
                st.rerun()

    # --- Histórico de aluguéis recentes ---
    st.subheader(T["recent"])
    for rental in st.session_state.recent_rentals:
        st.write(T["rented_msg"].format(rental["name"], rental["game"], rental["days"]))

    # --- Formulário de aluguel em outra aba ---
    if st.session_state.get("aba") == T["alugar_jogo"]:
        st.subheader(T["form_title"])
        # Lista de títulos dos jogos para o selectbox
        game_titles = [game["title"] for game in most_played_games]
        # Valor padrão: título do jogo selecionado anteriormente (se houver)
        default_game_title = None
        if st.session_state.get("selected_game"):
            default_game_title = st.session_state["selected_game"]["title"]
        selected_title = st.selectbox(
            T["select_game"],
            game_titles,
            index=game_titles.index(default_game_title) if default_game_title in game_titles else 0,
            key="selectbox_game"
        )
        # Atualiza o jogo selecionado conforme o selectbox
        selected_game = next(game for game in most_played_games if game["title"] == selected_title)
        st.session_state.selected_game = selected_game

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
                st.session_state.aba = T["biblioteca"]
                st.rerun()