# Quadtree Line Indexing with Range Query

Este proyecto implementa una estructura de datos **Quadtree** para indexar y gestionar líneas en un espacio 2D, permitiendo realizar consultas de búsqueda de líneas en un área circular y eliminar líneas dentro de esa área. Está implementado en Python utilizando la librería **Pygame** para la visualización gráfica.

## Características

- **Inserción de líneas**: Las líneas se insertan en el Quadtree y se subdividen según sea necesario cuando el número de líneas en una celda supera la capacidad del "bucket".
- **Consulta de líneas dentro de un rango circular**: Permite buscar las líneas que intersectan con un círculo de radio determinado centrado en la posición del mouse.
- **Eliminación de líneas dentro de un rango circular**: Permite eliminar las líneas que intersectan con el círculo de radio determinado.
- **Visualización interactiva**: Utiliza Pygame para mostrar la estructura del Quadtree y las líneas, con controles para activar la búsqueda, eliminación y agregar nuevas líneas.

## Requisitos

- Python 3.x
- Pygame (puedes instalarlo ejecutando `pip install pygame`)

## Cómo ejecutar el proyecto

1. Clona este repositorio o descarga el archivo.
2. Instala Pygame ejecutando el siguiente comando en la terminal:
   
   ```bash
   pip install pygame
    ```
## Ejecuta el archivo Python:
  ```bash
    python quadtree_lines.py
  ```
## Controles
- Tecla 'r': Activa la búsqueda de líneas dentro de un radio de un círculo centrado en el mouse.
- Tecla 'e': Activa la eliminación de líneas dentro de un radio de un círculo centrado en el mouse.
- Tecla 'i': Permite insertar nuevas líneas, solicitando al usuario la pendiente (slope) y el intercepto (intercepto) de la línea.
- Clic izquierdo: Elimina las líneas dentro del círculo cuando la eliminación está activada.
## Funcionalidad
Búsqueda: Al presionar la tecla 'r', puedes ver las líneas que están dentro de un círculo de radio alrededor del mouse.
Eliminación: Al presionar la tecla 'e', puedes eliminar las líneas dentro de un círculo de radio alrededor del mouse.
Inserción de líneas: Al presionar la tecla 'i', puedes agregar nuevas líneas especificando su pendiente e intercepto.
## Estructura del código
QuadtreeNode: Clase que representa un nodo del Quadtree. Contiene las líneas y puede subdividirse cuando su capacidad se excede.
Quadtree: Clase que representa el Quadtree completo y proporciona métodos para insertar, consultar y eliminar líneas.
main(): Función principal que maneja la inicialización de Pygame y la interacción con el usuario.
