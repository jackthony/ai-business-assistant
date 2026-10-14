# configs/ — configuración por tenant

Cada negocio (tenant) tiene su propia carpeta con su configuración:

configs/
├── hola_mujer/
│   ├── prompt.md      # prompt del sistema (identidad, tono, límites)
│   ├── rag.namespace   # namespace de ChromaDB (S6)
│   └── tools.json     # herramientas habilitadas (S7)
└── neuracode/
    └── ...

Regla: nada de secretos ni datos reales aquí — eso va en .env.
