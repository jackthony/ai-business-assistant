"""RAG sobre data/hola_mujer: solo entra lo aprobado y cada fragmento trae su procedencia."""

import json

from conftest import DATA

from rag.documents import _Servicio, load_documents, service_document
from rag.embedding import LexicalEmbedder
from rag.store import ChromaStore


def test_solo_servicios_activos_y_negocio_confirmado():
    docs = load_documents(DATA)
    assert len([d for d in docs if d.kind == "servicio"]) == 47
    assert {d.doc_id for d in docs if d.kind == "negocio"} == {
        "NEG-ADDRESS",
        "NEG-MAP_URL",
        "NEG-OPENING_HOURS",
    }


def test_promociones_inactivas_no_entran():
    assert not [d for d in load_documents(DATA) if d.kind == "promocion"]


def test_duracion_no_verificada_no_se_escribe():
    assert not [d for d in load_documents(DATA) if "Duración" in d.text]


def test_duracion_verificada_si_se_escribe():
    s = _Servicio(
        service_id="HM-X-001",
        categoria="Prueba",
        nombre="Servicio X",
        precio_pen=10,
        duracion_min=45,
        duracion_verificada=True,
    )
    assert "Duración: 45 minutos." in service_document(s).text


def test_servicio_sensible_sin_descripcion_clinica():
    raw = json.loads((DATA / "servicios.json").read_text(encoding="utf-8"))["items"]
    sensibles = {x["service_id"]: x for x in raw if x["sensible_clinico"]}
    docs = {d.doc_id: d for d in load_documents(DATA)}
    assert len(sensibles) == 21
    for sid, x in sensibles.items():
        assert docs[sid].sensitive
        if x["descripcion_corta"]:
            assert x["descripcion_corta"] not in docs[sid].text
        assert "S/" in docs[sid].text  # precio sí; explicación clínica no


def test_busqueda_trae_procedencia(store):
    top = store.search("precio taller PRP facial")[0]
    assert top.doc_id == "HM-ACA-001"
    assert top.source == "servicios.json#HM-ACA-001"
    assert top.label == "Taller PRP Facial + Capilar"


def test_sin_evidencia_devuelve_vacio(store):
    assert store.search("vuelo a marte") == []


def test_ingesta_reproducible(store):
    docs = load_documents(DATA)
    assert store.ingest(docs) == len(docs)
    assert store.ingest(docs) == len(docs)
    assert store.search("direccion local")[0].doc_id == "NEG-ADDRESS"


def test_namespaces_aislados():
    a = ChromaStore(LexicalEmbedder(), "ns-aislado-a")
    b = ChromaStore(LexicalEmbedder(), "ns-aislado-b")
    a.ingest(load_documents(DATA))
    b.ingest([])
    assert a.search("direccion local")
    assert b.search("direccion local") == []
