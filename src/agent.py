import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

import config

SYSTEM_PROMPT = """Sos un asistente interno para una empresa llamada SYNCRO que responde preguntas de empleados
basandote en los fragmentos de documento que se te dan como contexto, SIN AGREGAR INFORMACIÓN DE NINGUNA FUENTE EXTERNA.

Reglas:
1. Si la respuesta esta en el contexto, respondela de forma clara y directa, en español.
2. Si la pregunta del usuario es confusa, comunicale tu confusión y acompañalo con opciones (por ejemplo: 
PREGUNTA DEL USUARIO: "¿Qué es?"
3. Si el usuario dice o pregunta algo que no tiene que ver con los temas de tu documentación 
interna, podés improvisar una respuesta pero siempre manteniendo la seriedad y el profesionalismo.
TU RESPUESTA: No logro comprender qué necesitás saber. ¿Te interesa alguno de las siguientes temas?: *dar ejemplos de preguntas parecidas a la del usuario*).
4 Si la pregunta del usuario es completamente inentendible (por caracteres sin sentido o redacción sin sentido),
decilo explícitamente (por ejemplo: "No logro comprender tu preugnta, probá redactarla nuevamente")
5. Si entendés la pregunta del usuario pero no encontrás la respuesta en la documentación, 
decilo explícitamente (por ejemplo: "No cuento con esa información") 
6. No agregues datos que no esten en el contexto, aunque los sepas de otra fuente.
7. Si preguntan sobre tu identidad, responde lo que sabes según los documentos y según tu system prompt.

Contexto recuperado del documento:
{context}
"""

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{pregunta}"),
    ]
)


def crear_llm():
    return ChatGroq(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        api_key=config.GROQ_API_KEY,
        max_tokens= 300,
        timeout=30,
        max_retries=2,
    )


def formatear_contexto(documentos) -> str:
    partes = []
    for i, doc in enumerate(documentos, start=1):
        fuente = doc.metadata.get("source", "?")
        pagina = doc.metadata.get("page", "?")
        partes.append(f"[Fragmento {i} - {fuente}, página {pagina}]\n{doc.page_content}")
    return "\n\n".join(partes)


def responder_pregunta(pregunta: str, vectorstore, llm=None) -> dict:
    llm = llm or crear_llm()
    retriever = vectorstore.as_retriever(search_kwargs={"k": config.TOP_K})

    print(f"[{time.strftime('%H:%M:%S')}] Buscando documentos relevantes...", flush=True)
    documentos = retriever.invoke(pregunta)
    print(f"[{time.strftime('%H:%M:%S')}] Encontrados {len(documentos)} docs. Armando contexto...", flush=True)
    contexto = formatear_contexto(documentos)

    cadena = PROMPT | llm | StrOutputParser()
    print(f"[{time.strftime('%H:%M:%S')}] Llamando al LLM (Groq)...", flush=True)
    respuesta = cadena.invoke({"context": contexto, "pregunta": pregunta})
    print(f"[{time.strftime('%H:%M:%S')}] Respuesta generada.", flush=True)

    return {"respuesta": respuesta, "fuentes": documentos}
