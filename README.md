# Hackathon SmartDoc.ai 🚀

Bienvenue à la première édition du Hackathon SmartDoc.ai, organisé par l'Association des Alumni de l'École Centrale Casablanca (ECC Alumni)!

## À propos du Hackathon 📋

Ce hackathon se concentre sur le traitement automatique du langage naturel (NLP) et l'analyse de documents, en particulier les rapports SFCR des assureurs. Les participants devront développer des solutions innovantes pour:

1. Extraire et nettoyer le contenu pertinent des rapports PDF
2. Construire une architecture RAG (Retrieval-Augmented Generation) pour répondre à des questions spécifiques
3. [BONUS] Extraire les tableaux des rapports sous une forme structurée et lisible

Pour plus de détails sur les objectifs, les tâches et les exigences techniques, veuillez consulter le fichier [Instructions.docx](Instructions.docx).

## Prix 🏆

- **1er Prix**: 2500 MAD
- **2ème Prix**: 1000 MAD

## Comment Participer 🔧

### Soumission des Projets

1. Forkez ce repository
2. Créez un nouveau dossier avec le nom de votre équipe
3. Ajoutez votre travail dans ce dossier
4. Créez une Pull Request pour soumettre votre projet

### Structure du Dossier d'Équipe

Votre dossier doit contenir:
- Un fichier README.md avec:
  - Les noms des membres de l'équipe
  - Une description de votre solution
  - Les instructions d'installation et d'utilisation
- Vos notebooks Jupyter
- Le code source de votre solution
- Toute documentation supplémentaire

## Ressources 📚

- [helper.py](helper.py): Code auxiliaire pour le traitement des fichiers JSON
- [Trame_questions.pdf](Trame_questions.pdf): Ensemble de questions tests pour évaluer la performance de votre système RAG
- [data/](data/): Dossier contenant les données d'exemple
  - [data/pdfs/](data/pdfs/): Rapports SFCR au format PDF
  - [data/ocr/](data/ocr/): Fichiers JSON produits par l'OCR

Le fichier Trame_questions.pdf contient une série de questions prédéfinies qui seront utilisées pour évaluer la performance de votre système RAG. Assurez-vous que votre solution peut traiter efficacement ces questions tests.

## Dates Importantes ⏰

- **Début du Hackathon**: Samedi 7 décembre 2024
- **Date limite de soumission**: Samedi 14 décembre 2024 à 23:59 (heure marocaine)

Les participants doivent soumettre leurs pull requests avant la date limite. Toute soumission après cette date ne sera pas prise en compte.

## Contact 📧

Pour toute question ou clarification, n'hésitez pas à ouvrir une issue dans ce repository.

---

## SmartDoc AI – Full-Stack RAG App 🚀

This repo includes a production-ready RAG application for SFCR report analysis: upload PDFs, ask questions, get AI answers with citations, and view results as tables.

**Live demo:** https://smart-doc-ai-hackathon-98rp.vercel.app/

---

### How to run this project (step by step)

#### Prerequisites

- **Python 3.10+** (with `pip`)
- **Node.js 18+** (with `npm`)
- An **OpenAI API key** ([create one here](https://platform.openai.com/api-keys))

---

#### Step 1: Clone the repository

```bash
git clone https://github.com/Dead0Blue/Smart-doc-AI-hackathon.git
cd Smart-doc-AI-hackathon
```

---

#### Step 2: Set up the backend

1. Go into the backend folder:
   ```bash
   cd backend
   ```

2. Create a `.env` file in the `backend` folder with your OpenAI key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   (Replace `your_openai_api_key_here` with your real key.)

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   Leave this terminal open. You should see: `Uvicorn running on http://0.0.0.0:8000` and `Application startup complete.`

5. Check that it works: open **http://localhost:8000/** in your browser. You should see: `{"message":"Welcome to SmartDoc AI API"}`.

---

#### Step 3: Set up the frontend

1. Open a **new terminal** (keep the backend running in the first one).

2. From the **project root** (`Smart-doc-AI-hackathon`), go into the frontend folder:
   ```bash
   cd frontend
   ```

3. Install Node dependencies:
   ```bash
   npm install
   ```

4. Start the frontend dev server:
   ```bash
   npm run dev
   ```

5. Open the URL shown in the terminal (usually **http://localhost:5173**) in your browser.

---

#### Step 4: Use the app

1. **Upload a PDF** – Choose a SFCR or other PDF and click **Process document**.
2. **Ask a question** – Type a question in the text area and click **Ask** to get an AI answer with citations.
3. **Ask as table** – Click **Ask as table** to get the answer as structured JSON rows.
4. **Citations** – Click a citation chip to jump to the relevant part of the document (PDF viewer on the right).

---

#### Step 5 (optional): Deploy to the web

**Backend (e.g. Render)**

1. Go to [render.com](https://render.com) and sign in with GitHub.
2. **New +** → **Web Service** → select this repo.
3. Set **Root Directory** to `backend`.
4. **Build command:** `pip install -r requirements.txt`
5. **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. In **Environment**, add `OPENAI_API_KEY` (your key).
7. Deploy and copy your backend URL (e.g. `https://smartdoc-backend.onrender.com`).

**Frontend (Vercel)**

1. Go to [vercel.com](https://vercel.com) and import this repo.
2. Set **Root Directory** to `frontend`.
3. Add **Environment Variable:** `VITE_API_BASE` = your backend URL from Render.
4. Deploy. Your app will be live at the Vercel URL.

---

### Project structure

| Folder / file   | Purpose                                      |
|-----------------|----------------------------------------------|
| `backend/`      | FastAPI app, RAG (LangChain, ChromaDB), PDF processing |
| `frontend/`     | React + Vite UI (upload, chat, PDF viewer)   |
| `data/`         | Sample PDFs and OCR data                    |
| `Numero UNO/`   | Hackathon notebooks (RAG, tables)           |
| `render.yaml`   | Optional Render deployment config            |

---

Organisé avec ❤️ par ECC Alumni
