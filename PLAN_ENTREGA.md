# Plan de entrega del reporte

Objetivo: que el otro analista opere el reporte sin depender de Manuel, y que Manuel vea lo que pasa y pueda reparar cualquier daño.

## 1. Cómo queda armado

```
OneDrive / SharePoint de la empresa
└── Reporte Wellpro/             ← carpeta compartida: los dos con permiso de edición
    ├── Datos/                   ← lo que hoy es "Nueva versión": descargas y maestro
    ├── Reporte/                 ← el proyecto de Power BI (.pbip)
    └── Documentación/           ← manual, guías y definiciones
```

| Pieza | Dónde vive | Quién la cambia |
|---|---|---|
| Descargas diarias | `Datos/` | Los dos, según la rutina del manual |
| Maestro (productos, códigos, metas) | `Datos/Maestros/` | Los dos, solo para dar de alta productos o metas |
| Diseño del reporte (páginas, medidas) | `Reporte/`, con respaldo en GitHub | Solo Manuel |
| Reporte publicado | Área de trabajo de Power BI Service | Se actualiza solo |

**La carpeta debe estar en el OneDrive o SharePoint de la empresa, no en una cuenta personal.** Así no depende de una sola persona y la empresa conserva el acceso.

## 2. La rutina del otro analista (sin abrir Power BI Desktop)

1. Bajar los archivos del día y guardarlos en `Datos/`, como dice el manual.
2. El reporte publicado se **actualiza solo** a la hora programada (propuesta: 9:00 y 13:00), o con «Actualizar ahora» en Power BI Service.
3. Revisar la página **Control** en Power BI Service. Si está en 🟢, compartir.

Como no abre el proyecto, no puede dañar el diseño del reporte por accidente.

## 3. Cómo se entera Manuel y cómo repara

| Qué puede pasar | Cómo te enteras | Cómo se repara |
|---|---|---|
| Alguien borra o pisa un archivo | Alerta de la carpeta: en SharePoint, «Avisarme» cuando cambien o se borren archivos | **Papelera de reciclaje** (los archivos borrados se guardan unos 90 días) o **Historial de versiones** del archivo |
| Alguien daña el maestro | La misma alerta, y Control en 🔴 | Clic derecho en el maestro → **Historial de versiones** → restaurar la versión anterior |
| Falla la actualización programada | Correo automático de Power BI a los dos | Historial de actualizaciones en Power BI Service; el mensaje dice qué consulta falló |
| Faltan datos o hay un código nuevo | Página Control en 🔴 o 🟡 | La tabla de «Qué hacer según la página Control» del manual |
| Se daña el proyecto de Power BI | — | Se restaura desde GitHub, donde queda cada versión |

**Protección extra del maestro:** en Excel, **Revisar → Proteger libro**, para que nadie cambie el nombre de las hojas. El reporte las busca por nombre.

## 4. Pasos el día de la entrega

| # | Qué | Quién |
|---|---|---|
| 1 | Crear la carpeta compartida «Reporte Wellpro» en el SharePoint u OneDrive de la empresa y copiar `Nueva versión` como `Datos` | Manuel |
| 2 | Cambiar el reporte para que lea la carpeta compartida por su dirección de SharePoint y no por una ruta de la computadora. Así funciona igual para los dos y para la actualización programada. | Claude (con la dirección de la carpeta) |
| 3 | Publicar en un área de trabajo de Power BI Service; dar acceso al otro analista; configurar la actualización programada y los avisos de error | Manuel |
| 4 | Activar las alertas de la carpeta para Manuel | Manuel |
| 5 | Una sesión de 1 hora con el otro analista: hace la rutina del manual con Manuel al lado | Los dos |
| 6 | La primera semana, Manuel revisa la página Control cada día | Manuel |

## 5. Lo que hay que confirmar antes

1. **Licencias:** la actualización programada y compartir en un área de trabajo requieren **Power BI Pro** para los dos (o un área de trabajo Premium). Si no hay, el plan B es que quien actualiza abra Power BI Desktop, actualice y publique; el paso 2 también evita el problema de las rutas.
2. **Dónde se crea la carpeta:** en un sitio de SharePoint del área (lo ideal) o en el OneDrive de empresa de Manuel.
3. **Cómo ven el reporte los jefes:** hoy se comparte con un **enlace público**, que cualquiera con el enlace puede abrir. Se recomienda compartirlo desde el área de trabajo, solo con las personas autorizadas.
