import os
import shutil

import config
from src.loader import cargar_y_dividir_pdfs
from src.vectorstore import crear_vectorstore, cargar_vectorstore, indexacion_completa


def obtener_vectorstore():
    if indexacion_completa():
        print(f"Cargando vector store existente desde '{config.PERSIST_DIRECTORY}'...")
        return cargar_vectorstore()

    if os.path.isdir(config.PERSIST_DIRECTORY):
        print("Se encontro un indice incompleto de un intento anterior; se descarta.")
        shutil.rmtree(config.PERSIST_DIRECTORY)

    print(f"No hay un vector store previo. Procesando documentos en '{config.DATA_DIR}'...")
    chunks = cargar_y_dividir_pdfs()
    print(f"Documento dividido en {len(chunks)} fragmentos. Generando embeddings...")
    db = crear_vectorstore(chunks)
    print("Vector store creado y guardado. Las próximas ejecuciones van a ser más rápidas.\n")
    return db
