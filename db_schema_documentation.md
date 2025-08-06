# Simple‑Store‑Manager — Documentazione schema dati (PostgreSQL)

> Questa guida descrive tabelle, campi e relazioni del database di magazzino. Include anche un diagramma ER (formato Mermaid) da copiare in strumenti online come [**https://mermaid.live**](https://mermaid.live) per visualizzare graficamente lo schema.

---

## Indice

1. Tabelle anagrafiche
2. Tabelle operative
3. Tabelle log / storico
4. Diagramma ER completo (Mermaid)

---

## 1 · Tabelle anagrafiche

| Tabella              | Scopo                                                                       | Campi principali                                                                                                     |
| -------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **components**       | Anagrafica di **tutti** i pezzi stoccati (singoli o assemblati)             | `id UUID PK`, `sku TEXT UNIQUE`, `name TEXT`, `qr_code TEXT UNIQUE NULL`, `kind ENUM('RAW','ASSEMBLY')`, `unit TEXT` |
| **component\_parts** | Distinta base (BOM): lega i componenti **ASSEMBLY** alle loro parti **RAW** | `assembly_id FK→components.id`, `part_id FK→components.id`, `qty INTEGER`                                            |
| **suppliers**        | Fornitori di componenti                                                     | `id UUID PK`, `name TEXT`, `email TEXT`, `phone TEXT`                                                                |
| **users**            | Utenti applicazione (login)                                                 | `id UUID PK`, `username TEXT UNIQUE`, `password_hash TEXT`, `role ENUM('WAREHOUSE','ADMIN')`                         |

### Dettagli campi

- **components.kind** — distingue pezzi semplici (`RAW`) da assemblati (`ASSEMBLY`).
- **components.qr\_code** — presente solo per i pezzi che lo scanner deve rilevare.
- **component\_parts.qty** — quantità di part per ogni assembly (es. 1 molla per 1 pedalina).

---

## 2 · Tabelle operative

| Tabella             | Scopo                                    | Campi principali                                                                                                                                                  |
| ------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **stocks**          | Giacenze correnti per ciascun componente | `component_id PK/FK`, `qty_available INTEGER`, `updated_at TIMESTAMP`                                                                                             |
| **orders**          | Ordini da e‑commerce                     | `id UUID PK`, `shopify_id BIGINT`, `created_at_shop TIMESTAMP`, `prepared_at TIMESTAMP NULL`, `status ENUM('PENDING','IN_PICK','PREPARED')`, `customer_name TEXT` |
| **order\_lines**    | Righe ordine ↔ componenti                | `order_id FK`, `component_id FK`, `qty INTEGER`                                                                                                                   |
| **deliveries**      | Consegne fornitori                       | `id UUID PK`, `supplier_id FK`, `order_date DATE`, `received_date DATE NULL`, `has_issues BOOLEAN`, `notes TEXT`                                                  |
| **delivery\_lines** | Righe consegna ↔ componenti              | `delivery_id FK`, `component_id FK`, `qty_ordered`, `qty_received`                                                                                                |

### Flussi supportati

- **Evasione ordine**: quando un ordine passa a `PREPARED`, si genera decremento stock.
- **Ricezione consegna**: quando `received_date` viene impostata, si genera incremento stock.

---

## 3 · Tabelle log / storico

| Tabella                  | Scopo                          | Campi principali                                                                                                                                         |
| ------------------------ | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **inventory\_movements** | Log storico di tutti i ± pezzi | `id UUID PK`, `component_id FK`, `delta INTEGER`, `source_type ENUM('ORDER','DELIVERY','MANUAL')`, `source_id UUID`, `timestamp TIMESTAMP DEFAULT now()` |

> Questa tabella permette audit trail e statistiche (es. rotazione scorte).

---

## 4 · Diagramma ER (Mermaid)

```mermaid
erDiagram
    components {
        UUID id PK
        TEXT sku "UNIQUE"
        TEXT name
        TEXT qr_code "UNIQUE NULL"
        ENUM kind
        TEXT unit
    }
    component_parts {
        UUID assembly_id FK
        UUID part_id FK
        INT qty
    }
    stocks {
        UUID component_id PK FK
        INT qty_available
        TIMESTAMP updated_at
    }
    suppliers {
        UUID id PK
        TEXT name
        TEXT email
        TEXT phone
    }
    deliveries {
        UUID id PK
        UUID supplier_id FK
        DATE order_date
        DATE received_date
        BOOLEAN has_issues
        TEXT notes
    }
    delivery_lines {
        UUID delivery_id FK
        UUID component_id FK
        INT qty_ordered
        INT qty_received
    }
    orders {
        UUID id PK
        BIGINT shopify_id
        TIMESTAMP created_at_shop
        TIMESTAMP prepared_at
        ENUM status
        TEXT customer_name
    }
    order_lines {
        UUID order_id FK
        UUID component_id FK
        INT qty
    }
    inventory_movements {
        UUID id PK
        UUID component_id FK
        INT delta
        ENUM source_type
        UUID source_id
        TIMESTAMP timestamp
    }
    users {
        UUID id PK
        TEXT username "UNIQUE"
        TEXT password_hash
        ENUM role
    }

    components ||--o{ component_parts : has
    components ||--|| stocks : has
    components ||--o{ order_lines : appears_in
    components ||--o{ delivery_lines : appears_in
    components ||--o{ inventory_movements : moves

    orders ||--o{ order_lines : contains
    deliveries ||--o{ delivery_lines : contains

    suppliers ||--o{ deliveries : sends

    orders ||--o{ inventory_movements : generate
    deliveries ||--o{ inventory_movements : generate
```

---

**Come usare il diagramma**

1. Copia il blocco Mermaid in [https://mermaid.live](https://mermaid.live)
2. Visualizza il grafico ER o esportalo in SVG/PNG per la documentazione.

---

### Note progettuali

- Tutte le PK sono **UUID** per evitare collisioni e facilitare integrazioni future.
- Gli **ENUM** limitano i valori possibili e migliorano la leggibilità.
- La tabella `inventory_movements` funge da **append‑only log**: non si aggiorna mai, solo INSERT.
- La **foreign‑key cascade** è `ON DELETE RESTRICT` per componenti e `ON DELETE CASCADE` per linee figlie.

---

**Pronto per Copilot** Una volta che lo schema ti soddisfa ✔️→ ti fornirò il prompt SQLModel completo per generare classi, migrazioni e seed.

