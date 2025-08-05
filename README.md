# Simple-Store-Manager – Gestione semplificata del magazzino per piccole imprese

> **Un’applicazione web progressiva (PWA) per semplificare l’evasione ordini e l’aggiornamento delle giacenze tramite scanner QR e interfaccia intuitiva**

---

## Finalità

Simple-Store-Manager è pensata per aiutare piccole imprese (1–5 persone) a gestire in modo rapido e affidabile:

- **Evasione ordini** ricevuti da un sistema di e-commerce (Shopify o mock API).
- **Aggiornamento giacenze** quando arrivano nuovi componenti dai fornitori.
- **Tracciamento componenti** via scanner QRCode, riducendo errori manuali.

Con un’unica interfaccia PWA installabile come icona su smartphone e desktop, si riduce la curva di apprendimento e si evita la complessità delle app native.

---

## Requisiti funzionali

| RF-01 | **Login**: l’utente accede tramite credenziali(JWT-based).

| RF-02 | **Home**: due sezioni principali: “Ordini da evadere” e “Aggiorna giacenze”.

| RF-03 | **Elenco ordini**: lista di ordini con stato “pending” (Nuovo/In prelievo), visualizzata con ID, data e numero di pezzi.

| RF-04 | **Dettaglio ordine**: cliccando su un ordine, si mostra la lista di componenti da prelevare.

| RF-05 | **Scanner QR**: la camera inquadra codici QR per validare i componenti; accetta solo codici presenti nell’ordine e segnala errori in caso contrario.

| RF-06 | **Conferma prelievo**: ogni pezzo inquadrato si spunta nella lista; al completamento, si abilita il bottone “Conferma ordine preparato”.

| RF-07 | **Aggiorna stock**: sezione per incrementare/decrementare quantità a magazzino sia in input diretto sia con stepper (+1/–1).

| RF-08 | **Offline mode**: caching di ordini e movimenti con IndexedDB + Workbox Background Sync (Android).

| RF-09 | **PWA installabile**: manifest e service worker per installazione su Home e avvio in modalità standalone.

| RF-10 | **API REST**: backend FastAPI con endpoint CRUD per ordini, stock e login.

| RF-11 | **Database**: PostgreSQL schema con tabelle `components`, `orders`, `order_lines`, `stocks`, `users`.

---

## Architettura e tecnologie

- **Frontend**: PWA React + Vite (TypeScript)

  - Routing con `react-router-dom`
  - QR Scanner: API nativa `BarcodeDetector` + fallback `@zxing/browser`
  - Offline: Workbox (`workbox-window`) + IndexedDB (`idb-keyval`)
  - UI: componenti Material (oppure Tailwind/UI custom)

- **Backend**: FastAPI (Python 3.12)

  - ASGI server: Uvicorn
  - ORM: SQLModel
  - Autenticazione: JWT
  - PostgreSQL (versione 15/16)

- **Database**: PostgreSQL 15+

  - Schema relazionale per componenti, ordini e giacenze
  - Utente dedicato `magazzino` con permessi CRUD

- **Dev Tools**:
  - VS Code + GitHub Copilot (GPT-4o mini)
  - Linter/Formatter: ESLint + Prettier (frontend), Pylance + Ruff (backend)
  - Docker (opzionale) per orchestrazione locale

---

## Installazione

- **Clona il repository**:

  - git clone https://github.com/BonnaFra/Simple-Store-Manager.git
  - cd Simple-Store-Manager

- **Backend**:

  - cd backend
  - python3 -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt
  - createdb -U magazzino [company_name]\_magazzino
  - uvicorn main:app --reload

- **Frontend**:
  - cd ../frontend
  - npm install
  - npm run dev

---

## Utilizzo

1. Login con utente magazziniere
2. Seleziona “Ordini da evadere” per visionare gli ordini in attesa
3. Scansiona ogni codice QR per validare i componenti (messaggio di errore se non presenti)
4. Conferma ordine preparato → lo stato diventa prepared e le giacenze vengono aggiornate
5. Vai in “Aggiorna giacenze” per incrementare manualmente le quantità in ricezione

---

## Licenza

MIT © Francesco Bonini
