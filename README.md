## Agente RAG para Syncro

## Cómo funciona el widget flotante

`static/index.html` (con su header, chat y footer) es la **misma página**
que se sirve de dos formas distintas:

- Standalone, ocupando toda la pantalla, si entrás directo a `http://localhost:8501`
- Embebida dentro de una ventana flotante más chica, cuando `pagina_demo.html`
  la carga en un `<iframe>`

El botón "cerrar" que está en el header (dentro del chat) usa `postMessage`
para avisarle a la página exterior que cierre la ventana flotante — esto
funciona aunque el iframe y la página exterior estén en dominios distintos
(como pasa al abrir `pagina_demo.html` como archivo local mientras el
servidor corre en `localhost`).

## Cómo probarlo

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

copy .env.example .env          # Windows
# cp .env.example .env          # Mac/Linux
```

Completá `.env` con tus claves reales (`GOOGLE_API_KEY` y `GROQ_API_KEY`).

**1. Levantar el servidor del agente:**

```bash
python server.py
```

Esperá a que termine de indexar los PDFs (unos minutos la primera vez) y a que diga `Running on http://127.0.0.1:8501`.

**2. Probar el widget:**
Abrí `pagina_demo.html` con doble clic (en tu navegador, no en un panel de vista previa). Hacé clic en el botón verde lima de la esquina inferior derecha — el ícono cambia a una X cuando el chat está abierto.

## Estructura

```
.
├── data/                    # PDFs de ejemplo (reemplazar)
├── src/                     # logica del agente (sin cambios)
├── static/
│   ├── index.html           # interfaz del chat (header, burbujas, input)
│   ├── style.css            # tema oscuro + verde lima
│   └── script.js            # logica del chat + timestamps + postMessage
├── app.py                   # logica de carga/indexacion (sin cambios)
├── server.py                # servidor Flask (sin cambios)
├── pagina_demo.html         # pagina de relleno + boton flotante
├── requirements.txt / .env.example / .gitignore / .gitattributes
└── README.md
```
