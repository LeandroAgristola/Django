# Sistema de Gestión Integral para Estudios de Bienestar

## Descripción General del Proyecto

Este proyecto es un **sistema de gestión completo y modular** diseñado específicamente para estudios de bienestar (como estudios de yoga, pilates, fitness, etc.). Su objetivo es centralizar y simplificar todas las operaciones diarias, desde la captación de clientes a través de una web pública atractiva, hasta la administración interna detallada de clases, planes, personal, eventos y configuraciones generales.

El sistema se compone de un conjunto de aplicaciones Django interconectadas que trabajan en armonía para ofrecer una solución robusta y escalable, enriquecida con un frontend dinámico y estilizado gracias a CSS personalizado y scripts JavaScript para mejorar la experiencia de usuario.

## Filosofía del Sistema

* **Modularidad:** Cada aplicación se enfoca en un aspecto específico de la gestión, permitiendo un desarrollo y mantenimiento más sencillos.
* **Centralización:** Toda la información crítica se gestiona desde un panel de administración unificado, asegurando la coherencia de los datos.
* **Personalización:** Gran parte del contenido y comportamiento del sistema es configurable a través del panel de administración, minimizando la necesidad de modificar código para adaptaciones comunes.
* **Experiencia de Usuario:** Se prioriza una interfaz intuitiva y agradable tanto para el cliente final (`webPublic`) como para los administradores del estudio (`management`), con animaciones sutiles y un diseño responsive cuidado.

## Arquitectura del Sistema y Aplicaciones

El proyecto se estructura en las siguientes aplicaciones principales:

1.  **`webPublic` (Frontend Público):** La cara visible del estudio hacia los clientes.
2.  **`management` (Núcleo de Administración):** El corazón del panel de administración, gestionando la autenticación y la estructura base.
3.  **`configuracion` (Configuración Global):** Centraliza todos los ajustes y datos maestros del estudio.
4.  **`planes` (Gestión de Planes):** Administra los diferentes tipos de membresías y sus características.
5.  **`empleados` (Gestión de Staff):** Maneja la información del personal del estudio.
6.  **`calendario` (Gestión de Turnos):** Organiza la disponibilidad y asignación de turnos para clases regulares.
7.  **`eventos` (Gestión de Eventos):** Administra eventos especiales, talleres y workshops, incluyendo inscripciones.
8.  **`clientes` (Gestión de Clientes):** El CRM del sistema, manejando datos de clientes, sus planes, pagos y asistencia.

---

## 1. `webPublic` - El Portal de tu Estudio

**Descripción General:**
La aplicación `webPublic` es el frontend público del sistema. Su misión es presentar de forma atractiva toda la información relevante del estudio: detalles del espacio, planes ofrecidos, próximos eventos, el equipo de profesionales y vías de contacto. Toda la información mostrada es dinámica y se alimenta de las demás aplicaciones del sistema a través del panel de administración. La experiencia visual se define en `static/css/style.css` y se enriquece con interactividad mediante JavaScript.

**Características Principales:**

* **Página de Inicio (Home) Dinámica:**
    * Sección "Hero" con imagen y texto principal personalizables.
    * Apartado "Nosotros" para describir la filosofía y el espacio del estudio.
    * Visualización atractiva de planes activos con precios y botones de consulta directa (WhatsApp).
    * Sección de eventos destacados para promocionar actividades especiales.
    * Presentación del staff con fotografías y enlaces a perfiles sociales.
* **Página de Eventos Detallada:**
    * Listado completo de eventos activos con toda la información necesaria: fecha, hora, ubicación, descripción.
    * Información sobre cupos y métodos de pago.
    * Botones de inscripción directa vía WhatsApp con mensajes preconfigurados.
* **Diseño Totalmente Responsive:**
    * Adaptación fluida a dispositivos móviles, tablets y ordenadores de escritorio, gestionada por `style.css`.
    * Carrusel interactivo para la sección de staff en versiones móviles, también definido en `style.css`.
    * Menú hamburguesa animado para una navegación óptima en pantallas pequeñas, controlado por `static/js/menu-animations.js` y estilizado en `style.css`.
* **Experiencia de Usuario Mejorada:**
    * **Animaciones al Desplazar (Scroll):** Los elementos de las secciones aparecen suavemente a medida que el usuario navega, gracias al script `static/js/fadeInOnScroll.js`. Este script observa la intersección de los elementos con la clase `.fade-in` y les añade la clase `.visible` para activar la animación CSS definida en `style.css`.
    * **Botón Flotante de WhatsApp:** Un acceso directo y siempre visible para consultas, estilizado en `style.css`.
    * **Paleta de Colores y Tipografía Definida:** `style.css` establece una paleta de colores armónica (`#f6eddc`, `#e3e5d7`, `#bdd6d2`, `#a5c8ca`, `#586875`, `#3c4750`, `#283131`) y utiliza fuentes específicas ("Federo", "Faculty Glyphic", "Farro") para una identidad visual consistente.
* **Integraciones Clave:**
    * Enlaces directos a WhatsApp con mensajes predefinidos para facilitar la consulta y inscripción.
    * Conexión con perfiles de redes sociales (Instagram, Facebook, YouTube).
    * Integración de Google Maps para mostrar la ubicación exacta del estudio.

**Archivos Estáticos Clave para `webPublic`:**
* `static/css/style.css`: Hoja de estilos principal que define toda la apariencia visual, responsive design, paleta de colores, tipografías y estilos específicos para cada sección (hero, nosotros, planes, eventos, staff, footer, etc.).
* `static/js/fadeInOnScroll.js`: Implementa la funcionalidad de aparición gradual de elementos al hacer scroll, mejorando el dinamismo de la página.
* `static/js/menu-animations.js`: Controla el comportamiento del menú de navegación móvil (hamburguesa), su despliegue, cierre y la animación del botón.

**Dependencias de Modelos (para carga de datos):**
`Configuracion`, `Empleado`, `Evento`, `Plan`.

---

## 2. `management` - El Cerebro Administrativo

**Descripción General:**
La aplicación `management` es el núcleo del sistema de administración del estudio. Proporciona la infraestructura base para todas las operaciones de backend, incluyendo un sistema robusto de autenticación, un panel de control principal con estadísticas clave y la estructura de navegación para todos los módulos administrativos. La interfaz de esta sección está definida por `static/css/styleManagement.css`.

**Características Principales:**

* **Sistema de Autenticación Seguro:**
    * Página de login (`login.html`) con validación de credenciales, estilizada por `styleManagement.css` para integrarse con la estética del admin.
    * Protección de todas las rutas administrativas mediante el decorador `@login_required`.
    * Funcionalidad para cerrar sesión de forma segura.
* **Panel de Control (Dashboard) Interactivo (`panel.html`):**
    * Visualización de métricas clave del estudio mediante gráficos interactivos (Chart.js). Estos gráficos son cargados y actualizados dinámicamente por `static/js/panel_estadisticas.js`.
        * Movimiento anual de clientes (altas y bajas).
        * Disponibilidad diaria de turnos (ocupación del calendario).
        * Distribución de clientes por tipo de plan.
        * Participación y ocupación en eventos.
    * Filtros para personalizar la visualización de datos y rangos de fechas en los gráficos (funcionalidad provista por `panel_estadisticas.js`).
* **Estructura de Layout Unificada (`layout_management.html`):**
    * Barra lateral de navegación (`sidebar`) consistente para un acceso rápido a todos los módulos del sistema, con estilos definidos en `styleManagement.css`.
    * Sistema de mensajes y alertas (Django Messages) para feedback inmediato al usuario sobre las acciones realizadas.
    * Diseño responsive para una gestión eficiente desde cualquier dispositivo, asegurado por `styleManagement.css`.
* **Estilización Consistente:**
    * `styleManagement.css` define la apariencia de formularios, tablas, tarjetas de detalle (empleado, cliente, evento), modales y otros elementos comunes del panel de administración.

**Archivos Estáticos Clave para `management` y Módulos Administrativos:**
* `static/css/styleManagement.css`: Define la estética general del panel de administración, incluyendo el layout, sidebar, página de login, estilos para formularios, listados, tarjetas de detalle, el panel de estadísticas y el calendario.
* `static/js/panel_estadisticas.js`: Script fundamental para el dashboard. Realiza peticiones fetch a los endpoints de estadísticas de Clientes, Calendario, Planes y Eventos, y luego renderiza y actualiza los gráficos de Chart.js correspondientes.
* `static/js/metodo_pago.js`: Utilizado en formularios de creación/edición (ej. Eventos). Muestra u oculta dinámicamente el campo para el enlace de pago dependiendo si el precio es mayor a cero y si el método de pago seleccionado es "enlace".
* `static/js/validarFecha.js`: Script genérico para la validación de campos de fecha en formularios del lado del cliente, asegurando que no estén vacíos y añadiendo la clase `is-invalid` si es necesario.

**Flujo de Trabajo Típico del Administrador:**
1.  Acceso al sistema a través de la página de login.
2.  Redirección al panel de control principal tras una autenticación exitosa, donde `panel_estadisticas.js` carga los gráficos.
3.  Navegación a los diferentes módulos (Clientes, Eventos, Calendario, etc.) desde la barra lateral.
4.  Realización de operaciones CRUD, gestión de inscripciones, configuración, etc., utilizando formularios y listados estilizados por `styleManagement.css`.
5.  Recepción de feedback visual mediante el sistema de mensajes.
6.  Cierre de sesión seguro.

---

## 3. `configuracion` - Personalización Centralizada del Estudio

**Descripción General:**
La aplicación `configuracion` centraliza toda la configuración global del sistema y los datos fundamentales del estudio. Actúa como un panel de control maestro para personalizar la información que se muestra en la `webPublic` y define parámetros operativos clave (como horarios de apertura) que son utilizados por otras aplicaciones del sistema (ej. `calendario`, `clientes`). Los formularios y la presentación de datos se rigen por los estilos de `styleManagement.css`.

**Características Principales:**

* **Gestión Centralizada de Datos del Estudio:**
    * Nombre del estudio, dirección física, CUIT.
    * Información de contacto: teléfono, WhatsApp, email.
    * Enlaces a redes sociales: Instagram, Facebook, YouTube.
    * Enlace a Google Maps para la ubicación.
* **Configuración Operativa Detallada:**
    * Selección de días de la semana habilitados para la actividad.
    * Definición de horarios de apertura específicos para días de semana, sábados y domingos.
* **Contenido Dinámico para la Web Pública:**
    * Personalización del texto principal (sección "Hero") de la página de inicio.
    * Configuración de mensajes predefinidos para consultas por WhatsApp (utilizados en `webPublic` para planes y eventos).
* **Sistema Singleton:** Asegura que solo exista una instancia de configuración activa para todo el sistema, garantizando consistencia.
* **Validaciones Inteligentes:**
    * Verificación de coherencia en horarios (hora de inicio debe ser anterior a la hora de fin).
    * Requisito de seleccionar al menos un día habilitado para la operación del estudio.
    * Validación de formatos para URLs, emails y números de teléfono.
* **Interfaz de Administración Intuitiva:**
    * Formulario (`ConfiguracionForm`) con widgets amigables (ej. `MultiSelectField` para días habilitados, inputs de tiempo para horarios).
    * Organización lógica de los campos en el panel (`panel_config.html`) y formulario (`forms_config.html`) para fácil edición.
    * Modal de confirmación antes de guardar los cambios.

**Integraciones Clave:**
* **`webPublic`:** Provee todos los datos de contacto, redes, textos dinámicos y ubicación.
* **`calendario` y `clientes`:** Utilizan los días y horarios habilitados para la gestión de turnos y disponibilidad.
* **Sistema de Mensajería (WhatsApp):** Los mensajes predefinidos se usan para agilizar la comunicación desde la web.

---

## 4. `planes` - Gestión Estratégica de Membresías

**Descripción General:**
La aplicación `planes` permite la creación, edición y administración de los diferentes planes de membresía que ofrece el estudio. Estos planes definen las características, beneficios, frecuencia de asistencia, precio y visibilidad en la `webPublic`, siendo un pilar fundamental para la captación y gestión de clientes. La interfaz de administración se basa en `styleManagement.css`.

**Características Principales:**

* **Gestión Completa de Planes (CRUD):**
    * Creación y edición de planes detallando: nombre, descripción, precio y cantidad de días de asistencia por semana (1-7).
    * Control de estado (activo/inactivo) para una administración flexible de la oferta de planes.
    * Opción de mostrar/ocultar cada plan en la `webPublic`.
* **Funcionalidades Avanzadas:**
    * Formateo automático de precios para una visualización consistente en todo el sistema.
    * Propiedad `precio_formateado` en el modelo para fácil acceso.
    * Sistema de "papelera": los planes desactivados no se eliminan físicamente, permitiendo su reactivación.
    * Eliminación permanente de planes (con confirmación).
* **Validaciones Rigurosas:**
    * Asegura que la cantidad de días esté entre 1 y 7.
    * Campos requeridos validados para garantizar la integridad de los datos.
* **Estadísticas de Adopción:**
    * Vista (`estadisticas_planes`) que provee datos en formato JSON sobre cuántos clientes están suscritos a cada plan, útil para la toma de decisiones y visualizado en el dashboard mediante `panel_estadisticas.js`.
* **Interfaz de Usuario Clara:**
    * Listados separados para planes activos e inactivos (`lista_planes.html`).
    * Formulario unificado (`form_plan.html`) para creación y edición con validaciones visuales.
    * Modales de confirmación para acciones críticas (desactivar, eliminar).

**Integraciones Clave:**
* **`clientes`:** Los clientes se asocian a un plan, heredando sus restricciones y beneficios.
* **`webPublic`:** Muestra los planes activos y marcados como visibles al público.
* **`management`:** Todas las vistas están protegidas por el sistema de autenticación y `panel_estadisticas.js` consume sus datos para los gráficos.

---

## 5. `empleados` - Administración del Talento Humano

**Descripción General:**
La aplicación `empleados` se encarga del registro y la administración del personal del estudio. Permite gestionar perfiles completos, controlar su estado (activo/inactivo), su visibilidad en la `webPublic`, y mantener un historial de su trayectoria en el estudio. Su interfaz administrativa sigue los lineamientos de `styleManagement.css`.

**Características Principales:**

* **Modelo de Empleado Detallado:**
    * Datos personales: nombre, apellido, email, teléfono, dirección.
    * Datos laborales: fecha de alta, fecha de baja (opcional), estado activo/inactivo.
    * Perfil público: imagen de perfil, enlace a Instagram, y un switch para controlar la visibilidad en la `webPublic`.
* **Gestión Completa (CRUD) con "Papelera":**
    * Creación, lectura, actualización y eliminación de perfiles de empleados.
    * Desactivación lógica (movimiento a "papelera") con registro de fecha de baja, conservando el historial.
    * Posibilidad de reactivar empleados, limpiando la fecha de baja y actualizando la fecha de alta si es necesario.
    * Eliminación permanente (con confirmación y eliminación automática de la imagen asociada).
* **Control de Visibilidad en Web:**
    * Se puede definir qué empleados aparecen en la sección "Staff" de la `webPublic`.
    * Validación para limitar el número de empleados visibles en la web (configurable, actualmente 4) para mantener un diseño equilibrado.
* **Validaciones Específicas:**
    * Nombre y apellido solo pueden contener letras.
    * Teléfono solo admite números.
    * Formato de email válido.
* **Gestión de Imágenes de Perfil:**
    * Subida de imágenes de perfil.
    * Eliminación automática de la imagen del sistema de archivos cuando el empleado es eliminado permanentemente o se cambia su imagen.
* **Interfaz de Administración Eficaz (`lista_empleados.html`, `tarjetaEmpleado`):**
    * Tablas separadas para empleados activos e inactivos.
    * Modales interactivos para confirmación de acciones (desactivación, reactivación, eliminación) y para el formulario de creación/edición.
    * Vista de tarjeta para detalle de empleado.

**Integraciones Clave:**
* **`webPublic`:** Muestra la información e imagen de los empleados marcados como "visibles".
* **`management`:** Todas las vistas requieren autenticación.
* **Sistema de Archivos de Django:** Para el almacenamiento y gestión de `MEDIA_ROOT` (imágenes de perfil).

---

## 6. `calendario` - Optimización de Horarios y Turnos

**Descripción General:**
La aplicación `calendario` gestiona el sistema de turnos del estudio, permitiendo una visualización clara de la disponibilidad por día y hora, la gestión detallada de los turnos asignados a clientes, y el análisis de estadísticas de ocupación. Se integra estrechamente con la configuración general del estudio y el módulo de clientes. La visualización del calendario y sus estadísticas se apoya en `styleManagement.css` y `panel_estadisticas.js`.

**Características Principales:**

* **Modelo de Turnos (`Turno`):**
    * Almacena fecha, hora y la relación con el `Cliente` asignado.
    * Validaciones para evitar la duplicación de turnos para un mismo cliente en el mismo horario.
    * Ordenamiento natural por fecha y hora.
* **Visualización de Calendario Interactivo (`calendario.html`):**
    * Integración con **FullCalendar** para una vista mensual intuitiva, estilizada para coherencia con `styleManagement.css`.
    * Indicación visual de disponibilidad diaria:
        * Colores para identificar días con cupos, llenos, o parcialmente ocupados.
    * Permite seleccionar un día para ver el detalle de horarios.
* **Gestión Detallada de Turnos por Día (`detalle_dia.html`):**
    * Muestra los turnos por franja horaria para un día específico.
    * Capacidad máxima configurable por hora (actualmente 6 turnos/hora).
    * Considera automáticamente los días y horarios de apertura definidos en la `Configuracion` del estudio.
* **Endpoints JSON para Dinamismo:**
    * `disponibilidad_por_dia`: Provee datos a FullCalendar sobre la ocupación de cada día.
    * `horarios_por_dia`: Devuelve los horarios disponibles para un día seleccionado, considerando la capacidad y los turnos ya asignados.
* **Estadísticas de Ocupación (`estadisticas_turnos`):**
    * Genera datos para gráficos (Chart.js) sobre:
        * Ocupación promedio por día de la semana.
        * Comparativa de ocupación entre el mes actual y el próximo.
    * Estos datos son consumidos y visualizados por `panel_estadisticas.js` en el dashboard.

**Integraciones Clave:**
* **`configuracion`:** Utiliza los `dias_habilitados` y los horarios de apertura para determinar la disponibilidad.
* **`clientes`:** Se relaciona con el modelo `Cliente` para asignar turnos.
* **`management`:** Todas las vistas requieren autenticación, y el dashboard muestra sus estadísticas.

**Flujo de Trabajo para Administradores:**
1.  Acceder a la vista del calendario.
2.  Visualizar la ocupación general del mes.
3.  Seleccionar un día específico para ver el detalle de turnos por hora.
4.  Identificar horarios disponibles o llenos.
5.  Consultar estadísticas en el dashboard para la toma de decisiones sobre horarios y clases.
    *(Nota: La asignación de turnos a clientes se realiza principalmente desde el módulo `clientes`)*

---

## 7. `eventos` - Gestión Profesional de Actividades Especiales

**Descripción General:**
La aplicación `eventos` es un sistema completo para la gestión de eventos especiales, talleres, o workshops. Cubre todo el ciclo de vida del evento, desde su creación y promoción en la `webPublic`, hasta la administración de inscripciones, control de cupos, gestión de pagos y generación de reportes. Los formularios y listados se estilizan con `styleManagement.css`, y la lógica de mostrar/ocultar campos de pago se maneja con `metodo_pago.js`.

**Características Principales:**

* **Gestión Completa de Eventos (CRUD):**
    * Creación y edición detallada: título, descripción, fecha, hora, ubicación, imagen destacada.
    * Sistema de cupos con control de disponibilidad en tiempo real.
    * Configuración de métodos de pago: enlace de pago externo o pago en el estudio. El campo para el enlace de pago aparece condicionalmente gracias a `metodo_pago.js`.
    * Control de visibilidad en la `webPublic` (con límite configurable).
* **Sistema Avanzado de Inscripciones:**
    * Inscripción de clientes existentes (búsqueda optimizada con Select2).
    * Registro de nuevos clientes directamente desde el formulario de inscripción del evento, integrándose con la app `clientes`.
    * Gestión de estados de pago para cada inscripción (pendiente/confirmado).
    * Liberación automática de cupos al cancelar una inscripción.
* **Herramientas de Administración y Reportes:**
    * "Papelera" de eventos: permite desactivar eventos finalizados o pasados sin eliminarlos, conservando el historial y permitiendo su reactivación.
    * Eliminación permanente de eventos.
    * **Exportación a PDF del listado de inscriptos:** Generación de informes profesionales (usando ReportLab) con detalles de los participantes, estado de pago y logo del estudio.
    * Estadísticas de ocupación y participación en eventos, visualizadas en el dashboard mediante `panel_estadisticas.js`.
* **Validaciones Inteligentes:**
    * Validación de fechas (fecha del evento no puede ser en el pasado al crearlo), potencialmente asistida por `validarFecha.js`.
    * Consistencia en métodos de pago.

**Integraciones Clave:**
* **`clientes`:** Para la gestión de los participantes (existentes o nuevos).
* **`webPublic`:** Para mostrar los eventos activos y promocionarlos.
* **`management`:** Todas las vistas administrativas están protegidas, y `panel_estadisticas.js` consume sus datos.
* **`configuracion`:** Podría usar datos del estudio para los PDFs (ej. nombre del estudio).

**Flujo de Trabajo Típico:**
1.  **Creación del Evento:** El administrador completa el formulario. Si el evento tiene precio, `metodo_pago.js` muestra opciones de método de pago.
2.  **Promoción:** El evento se muestra en la `webPublic` si está marcado como visible.
3.  **Inscripción de Clientes:**
    * Desde el panel de admin, se pueden inscribir clientes existentes o registrar nuevos.
    * Se actualiza el estado de pago y los cupos disponibles.
4.  **Seguimiento:** El administrador monitorea las inscripciones y la ocupación.
5.  **Durante el Evento:** Se puede usar el listado de PDF para control de asistencia.
6.  **Post-Evento:** Se desactiva el evento (mueve a la papelera) y se analizan estadísticas en el dashboard.

---

## 8. `clientes` - El Corazón de la Relación con tus Miembros

**Descripción General:**
La aplicación `clientes` es el sistema CRM (Customer Relationship Management) del estudio. Permite un registro y gestión exhaustiva de los clientes, desde sus datos personales hasta la asignación de planes, el control de sus turnos recurrentes, la gestión de pagos y el seguimiento de su actividad. Es fundamental para la operativa diaria y la fidelización. Se apoya en `styleManagement.css` para la interfaz y `panel_estadisticas.js` para mostrar sus métricas.

**Características Principales:**

* **Modelo de Cliente Avanzado (`Cliente`):**
    * Datos personales completos, DNI (único), email (único), contacto.
    * Tipos de cliente (Ej: Regular, Eventual).
    * Estados de pago (Ej: Pendiente, Confirmado, Vencido) con lógica de cálculo automático.
    * Relación con `Planes` para definir su membresía.
    * Gestión de turnos asignados (días y horarios específicos).
    * Control de fechas de alta y baja, con historial.
    * Propiedades calculadas (ej. fecha de vencimiento de cuota, estado de pago actual).
* **Gestión Integral de Clientes (CRUD):**
    * Creación, edición, visualización detallada (`detalle_cliente.html`, estilizado como `tarjetaCliente` en `styleManagement.css`).
    * Listado de clientes (`lista_clientes.html`) con filtros avanzados (por estado, plan, etc.).
    * Desactivación y reactivación de clientes con mantenimiento de historial.
    * Eliminación permanente.
* **Flujo Optimizado de Asignación de Turnos (2 Pasos):**
    * Interfaz especializada (`asignar_turnos.html`) para seleccionar días y horarios.
    * Validación en tiempo real de disponibilidad de turnos (integrado con `calendario` y `configuracion`).
    * Persistencia de datos entre pasos usando sesiones de Django.
    * Visualización clara de turnos ocupados/disponibles.
    * Coherencia automática con las restricciones del plan del cliente (ej. cantidad de días).
* **Generación Automática de Turnos Futuros:**
    * Al asignar turnos, el sistema puede generar automáticamente los turnos recurrentes para los próximos 6 meses (configurable).
    * Respeta los días y horarios asignados y los días habilitados en la `configuracion` del estudio.
* **Gestión de Pagos y Estados:**
    * Confirmación manual de pagos mensuales.
    * El estado de pago se actualiza automáticamente: "Confirmado" si se paga en el mes, "Vencido" si no se paga después de una fecha límite (ej. día 7), "Pendiente" por defecto.
    * Comando de gestión (`resetear_estados_mensual`): Tarea programada para ejecutar el primer día de cada mes y reiniciar los estados de pago a "Pendiente", facilitando el nuevo ciclo de cobro.
* **Validaciones Avanzadas:**
    * Unicidad de DNI y email.
    * Disponibilidad de turnos al momento de la asignación.
    * Coherencia entre el plan seleccionado y los días/horarios asignados.
    * Validación de fechas con `validarFecha.js` en formularios relevantes.
* **Estadísticas e Informes:**
    * Datos sobre movimiento mensual de clientes (altas/bajas).
    * Total de clientes activos, por plan, etc. (vista `clientes_estadisticas` consumida por `panel_estadisticas.js` para el dashboard).
    * Potencial para exportación de datos.

**Integraciones Clave:**
* **`calendario`:** Para verificar disponibilidad y crear instancias de `Turno`.
* **`planes`:** Para asociar clientes a membresías y aplicar sus reglas.
* **`configuracion`:** Para respetar días/horarios de apertura del estudio al generar turnos.
* **`eventos`:** Clientes eventuales pueden ser registrados a través de eventos.
* **`management`:** Autenticación, layout base y visualización de estadísticas en dashboard.
* **Sistema de Sesiones de Django:** Para el flujo de asignación de turnos.
* **Sistema de Mensajes de Django:** Para feedback al usuario.

**Flujo de Trabajo Completo (Ejemplo Alta de Cliente):**
1.  **Ingreso de Datos Básicos:** Nombre, apellido, DNI, contacto, email.
2.  **Selección de Plan:** Se elige el plan que el cliente va a adquirir.
3.  **Asignación de Turnos (Flujo Especializado):**
    a.  Selección de días de la semana (limitado por el plan).
    b.  Elección de horarios disponibles para cada día seleccionado (validación en tiempo real).
    c.  Confirmación.
4.  **Generación Automática:** El sistema crea los objetos `Turno` para los próximos 6 meses.
5.  **Gestión Mensual:** El administrador confirma el pago del cliente, y el sistema actualiza su estado. El comando `resetear_estados_mensual` prepara el ciclo siguiente.

---

## Tecnologías Utilizadas (Stack General)

* **Backend:**
    * Python
    * Django Framework (ORM, Forms, Authentication, Admin, Templates DTL, etc.)
* **Frontend (Público y Admin):**
    * HTML5
    * CSS3 (con archivos `style.css` y `styleManagement.css` personalizados)
    * Bootstrap 5 (para diseño responsive y componentes UI)
    * JavaScript (para animaciones, efectos, interactividad y lógica de cliente, incluyendo `fadeInOnScroll.js`, `menu-animations.js`, `metodo_pago.js`, `panel_estadisticas.js`, `validarFecha.js`)
* **Bases de Datos:** (Compatible con las soportadas por Django: PostgreSQL, MySQL, SQLite, etc.)
* **Librerías Adicionales Destacadas:**
    * **Chart.js:** Para gráficos interactivos en los paneles de administración (controlados por `panel_estadisticas.js`).
    * **FullCalendar:** Para la visualización del calendario de turnos.
    * **Font Awesome:** Para iconografía en toda la aplicación.
    * **Google Fonts:** Para una tipografía web moderna y legible (definidas en `style.css`).
    * **ReportLab:** Para la generación de reportes en PDF (listado de inscriptos a eventos).
    * **Select2:** Para campos de selección con búsqueda avanzada (ej. selección de clientes en inscripciones a eventos).
    * **django-multiselectfield:** Para campos de selección múltiple amigables (ej. días habilitados en `configuracion`).

---

## Puntos Clave de Desarrollo y Configuración

* **Panel de Administración Centralizado:** La mayoría de los datos y contenidos son gestionables desde el admin de Django, permitiendo modificar el contenido sin tocar el código.
* **Estructura de Plantillas:**
    * `webPublic` utiliza `layout.html` como plantilla base.
    * Todos los módulos de administración (`management`, `calendario`, `clientes`, etc.) heredan de `layout_management.html` para una interfaz consistente.
* **Estilos y Scripts:**
    * CSS globales y específicos en `/static/css/` (`style.css`, `styleManagement.css`).
    * Imágenes estáticas en `/static/img/`.
    * Scripts JS en `/static/js/` (incluyendo los analizados: `fadeInOnScroll.js`, `menu-animations.js`, `metodo_pago.js`, `panel_estadisticas.js`, `validarFecha.js`).
    * Logo y favicon en `/static/logo/`.
* **Seguridad:** Uso extensivo del decorador `@login_required` de Django para proteger todas las vistas administrativas.
* **Feedback al Usuario:** El sistema de `messages` de Django se utiliza para proporcionar notificaciones sobre el resultado de las acciones.
* **Gestión de Archivos:** `MEDIA_ROOT` debe estar correctamente configurado para el almacenamiento de imágenes subidas por los usuarios (ej. fotos de perfil de empleados, imágenes de eventos).

---

## Consideraciones para Producción

* **Tarea Programada (Cron Job):** Es crucial configurar la tarea `resetear_estados_mensual` (del módulo `clientes`) para que se ejecute automáticamente el primer día de cada mes.
* **Configuración de `MEDIA_ROOT` y `STATIC_ROOT`:** Asegurar que las rutas para archivos estáticos y de medios estén correctamente configuradas y sean servidas eficientemente por el servidor web (Nginx, Apache).
* **Variables de Entorno:** Utilizar variables de entorno para configuraciones sensibles (SECRET_KEY, configuración de base de datos, API keys si las hubiera).
* **Seguridad:** Revisar la configuración de `DEBUG` (debe ser `False` en producción), `ALLOWED_HOSTS`, y otras directivas de seguridad de Django.
* **Capacidad del Servidor:** Considerar la carga para generación de PDFs y el manejo de múltiples usuarios concurrentes.

