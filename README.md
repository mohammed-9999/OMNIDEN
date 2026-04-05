![Omniden Logo](./logo.svg)


# Omniden 🛒

**Omni Market. One Eye**

**Omniden** is an intelligent product discovery tool designed to streamline your online shopping experience. Instead of hopping between dozens of tabs, users simply enter the product they are looking for, and Omniden crawls multiple e-commerce platforms to bring the best results directly to them.

## 🚀 Features
* **Unified Search:** Search across multiple marketplaces from a single interface.
* **Real-time Results:** Get the latest pricing and availability.
* **Simplified UI:** No more clutter—just the products you want.

## 🏗️ Project Architecture

```
omniden/
├── backend/
│   ├── docker/                  # Infrastructure Docker
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   └── .env.postgres
│   │
│   ├── src/
│   │   ├── main.py              # Point d'entrée
│   │   ├── celery_app.py        # Initialisation de l'application Celery
│   │   │
│   │   ├── routes/
│   │   │   ├── search.py        # Endpoints pour lancer la recherche via Gemini
│   │   │   └── products.py      # Endpoints pour récupérer les résultats
│   │   │
│   │   ├── controllers/         # Le cerveau adapté à l'IA
│   │   │   ├── search_orchestrator.py   # Orchestre la requête utilisateur et fait appel à Gemini
│   │   │   └── gemini_controller.py     # Gère la communication directe avec l'API Gemini (parsing, requêtes)
│   │   │
│   │   ├── models/
│   │   │   ├── schemas/
│   │   │   │   ├── product.py   # Structure du produit standardisé par Gemini
│   │   │   │   └── search.py
│   │   │   ├── db_schemas/
│   │   │   └── enums/
│   │   │
│   │   ├── helpers/
│   │   │   ├── config.py        # Chargement de la configuration (inclut GEMINI_API_KEY)
│   │   │   └── prompts.py       # Stockage et gestion des templates de prompts pour Gemini
│   │   │
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   └── gemini_tasks.py  # Appels asynchrones à l'API Gemini via Celery
│   │   │
│   │   └── stores/              # Interfaces vers des services externes (bases vectorielles, API tierces)
│   │
│   ├── assets/
│   ├── tests/
│   ├── .env                     # Variables d'environnement (clé API Gemini, etc.)
│   ├── .env.example
│   ├── .gitignore
│   └── requirements.txt         # Inclut le SDK Google Generative AI
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── store/
│   │   └── types/
│   ├── public/
│   ├── tailwind.config.js
│   └── package.json
│
└── README.md
```

## 🛠️ Tech Stack
* **Backend:** Python (FastAPI), Celery for async task processing
* **AI / Search:** Google Gemini API with Search Grounding
* **Database:** PostgreSQL (via Docker)
* **Frontend:** Next.js with Tailwind CSS

## ⚙️ Setup & Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mohammed-9999/Omniden.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd Omniden
    ```
3.  **Install dependencies:**
    *(Add instructions here once the framework is chosen)*

## 📈 Roadmap
- [ ] Initial project architecture.
- [ ] Integration with major e-commerce APIs.
- [ ] User authentication system.
- [ ] Price tracking and alerts.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/mohammed-9999/Omniden/issues).

---
*Developed by [Mohammed](https://github.com/mohammed-9999)*
