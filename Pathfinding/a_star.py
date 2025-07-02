import time
import heapq
from typing import Tuple, Callable
from dataclasses import dataclass
from collections import defaultdict

import tkinter as tk
from tkinter import messagebox




@dataclass
class Node:
  "Representa un nodo en el algoritmo A*"
  position: tuple[int,int]   # posición en el grid
  
  g_score: int  # coste del camino desde el nodo inicio al nodo actual 
  h_score: int  # coste estimado del camino desde el nodo actual al objetivo/meta
  parent: 'Node' = None
  
  def __post_init__(self):
    self.f_score:int = self.g_score + self.h_score  

  def __lt__(self, other:'Node'):
    if not isinstance(other, Node): raise Exception(f"other is: {type(other)}, not Node")
    return self.f_score < other.f_score

  def __eq__(self, other:'Node'):
    if not isinstance(other, Node): raise Exception(f"other is: {type(other)}, not Node")
    return self.position == other.position



#region: HEURISTIC Functions
def manhattan_distance(pos1:Tuple, pos2:Tuple) -> int:
  "Calcula la distancia Manhattan entre dos posiciones"
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

#endregion



#region: CONSTANTS
TITLE = "Algoritmo A*"
COLORS = {
  0: "white", # vacío
  1: "black", # obstáculo
  2: "green", # inicio
  3: "red",   # objetivo/meta
  "open": "lightblue",    # nodos en lista abierta 
  "visiting": "orange",   # nodo siendo visitado
  "closed": "lightcoral", # nodos visitados (lista cerrado)
  "path": "yellow"        # camino final
}
#endregion




#region: VISUALIZER
class AStar_Visualizer:
  """Visualizador del Algoritmo A* a partir de una cuadrícula (grid)
  
  Estados de cada celda:
      0=vacío
      1=obstáculo     ('obstacle')
      2=inicio        ('start')
      3=objetivo/meta ('goal')
  """
  
  def __init__(self, h_function, cell_size:int=25, width=30, height=20) -> None:
    """Configurar los parámetros de la Interfaz, considerando tamaño de la celda y cantidad de celdas en la cuadrícula

    Args:
        cell_size (int, optional): cantidad de celdas en el grid. Defaults to 25.
        width/height (int, optional): tamaño de cada celda. Defaults to 30/20.
    """
    
    self.h_function:Callable[[Tuple, Tuple], int] = h_function
    
    self.width:int  = width
    self.height:int = height
    self.cell_size:int = cell_size
    self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Estados
    self.start = None 
    self.goal = None
    self.mode = "obstacle" # 'obstacle', 'start', 'goal'
    
    self.colors = COLORS
    self.setup_gui()
  
  def setup_gui(self) -> None:
    self.root = tk.Tk()
    self.root.title(TITLE)
    self.root.resizable(False,False)
    
    # frame para controles
    control_frame = tk.Frame(self.root)
    control_frame.pack(pady=10)
    
    # botones de modo
    tk.Button(control_frame, 
      text="Obstáculos",
      command=lambda: self.set_mode("obstacle")
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, 
      text="Inicio",
      command=lambda: self.set_mode("start")
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, 
      text="Objetivo",
      command=lambda: self.set_mode("goal")
    ).pack(side=tk.LEFT, padx=5)
    
    # botones de acción
    tk.Button(control_frame, 
      text="Ejecutar A*",
      command=self.run_astar, bg="lightgreen"
    ).pack(side=tk.LEFT, padx=10)
    tk.Button(control_frame, 
      text="Limpiar*",
      command=self.clear_grid
    ).pack(side=tk.LEFT, padx=5)
    
    # canvas para el grid
    self.canvas = tk.Canvas(
      self.root,
      width = self.width  * self.cell_size,
      height= self.height * self.cell_size,
      bg="white"
    )
    self.canvas.pack(pady=10)

    # utiles para on-drag
    self.current_cel_x = -1
    self.current_cel_y = -1
    
    # eventos del mouse
    self.canvas.bind("<Button-1>", self.on_click)
    self.canvas.bind("<B1-Motion>", self.on_drag)
    
    # label de información
    self.info_label = tk.Label(
      self.root,
      text="Visualización del Algoritmo A* incorporando obstáculos, una celda de inicio y un objetivo",
    )
    self.info_label.pack()
    
    self.draw_grid()
  
  def set_mode(self, mode:str) -> None:
    self.mode = mode 
    mode_text = {
      "obstacle": "Modo: Obstáculo",
      "start":    "Modo: Inicio",
      "goal":     "Modo: Meta",
    }
    self.info_label.config(text=mode_text[self.mode])
  
  def on_click(self, event) -> None:
    col = event.x // self.cell_size
    row = event.y // self.cell_size
    
    if 0 <= row < self.height and 0 <= col < self.width:
      
      if self.mode == "obstacle":
        self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0
      
      if self.mode == "start":
        if self.start:
          old_row,old_col = self.start
          self.grid[old_row][old_col] = 0
        self.start = (row, col)
        self.grid[row][col] = 2 
      
      if self.mode == "goal":
        if self.goal:
          old_row,old_col = self.goal
          self.grid[old_row][old_col] = 0
        self.goal = (row,col)
        self.grid[row][col] = 3
    
    self.draw_grid()
  
  def on_drag(self, event):
    cel_x = event.x // self.cell_size
    cel_y = event.y // self.cell_size
    
    if cel_x == self.current_cel_x and cel_y == self.current_cel_y:
      return 
    if self.mode == "obstacle":
      self.current_cel_x = cel_x
      self.current_cel_y = cel_y
      self.on_click(event)
  
  def get_neighbors(self, pos):
    "Obtiene los vecinos válidos de una posición"
    row,col = pos 
    neighbors = []
    
    directions = [  
      (-1,  0),  # arriba  
      ( 1,  0),  # abajo 
      ( 0, -1),  # izquierda
      ( 0,  1)   # derecha
    ]
    
    for dr,dc in directions: 
      new_row,new_col = row + dr, col + dc 
      
      if (0 <= new_row < self.height and 
          0 <= new_col < self.width  and 
          self.grid[new_row][new_col] != 1):
        neighbors.append( (new_row,new_col) )
    return neighbors
  
  def reconstruct_path(self, node:Node):
    "Reconstruye el camino desde el nodo meta hasta el inicio"
    path = []
    current = node 
    while current:
      path.append(current.position)
      current = current.parent
    return path[::-1]
  
  def _astar(self):
    "Implementación del algoritmo A*"
    if not self.start or not self.goal: return None,[],[],[]

    open_list  = []
    open_set   = set()
    closed_set = set()
    
    # diccionario para rastrear el mejor costo g para cada posición
    g_costs = defaultdict(lambda: float('inf'))
    
    # nodo inicial
    start_node = Node(
      position=self.start,
      g_score=0,
      h_score=self.h_function(self.start, self.goal)
    )
    
    heapq.heappush(open_list, start_node)
    open_set.add(self.start)
    g_costs[self.start] = 0
    
    search_steps = [] # para visualización: almacenar estados 
    
    while open_list:
      # obtener el nodo con menor f
      current_node:Node = heapq.heappop(open_list)
      open_set.discard(current_node.position)
      
      # si se llega a la meta
      if current_node.position == self.goal:
        path = self.reconstruct_path(current_node)
        return path, search_steps, list(closed_set), list(open_set)
      
      # mover a la lista cerrada
      closed_set.add(current_node.position)
      
      # guardar estado actual para visualización
      search_steps.append({
        'current':current_node.position,
        'open':   open_set.copy(),
        'closed': closed_set.copy()
      })
      
      # explorar vecinos
      for neighbor_pos in self.get_neighbors(current_node.position):
        if neighbor_pos in closed_set: continue
        
        # calcular nuevo costo g
        tentative_g = current_node.g_score + 1 # costo uniforme de 1 
        
        # si se encuentra un mejor camino a este vecino
        if tentative_g < g_costs[neighbor_pos]:
          g_costs[neighbor_pos] = tentative_g
          h_cost = self.h_function(neighbor_pos, self.goal)
          neighbor_node = Node(
            position=neighbor_pos,
            g_score=tentative_g,
            h_score=h_cost,
            parent=current_node
          )
          heapq.heappush(open_list, neighbor_node)
          open_set.add(neighbor_pos)
    
    return None, search_steps, list(closed_set), list(open_set)
    
  def run_astar(self):
    "Ejecutar A* y visualizar el proceso"
    if not self.start or not self.goal:
      messagebox.showwarning("Advertencia", "Se necesita establecer el punto de inicio y el punto del objetivo")
      return 

    self.info_label.config(text="Ejecutando A*...")
    self.root.update()
    
    path, search_steps, _, _ = self._astar()
    
    if path:
      self.visualize_search(search_steps, path)
      self.info_label.config(text=f"Camino encontrado con longitud {len(path)} pasos")
    else: 
      messagebox.showinfo("Sin solución", "No se encontró un camino hacia la meta")
      self.info_label.config(text="No hay camino disponible")
      
  
  def visualize_search(self, search_steps, path):
    "Visualiza el proceso de búsqueda paso a paso"
    # animar cada paso del algoritmo
    for step in search_steps:
      current_pos = step['current']
      open_nodes = step['open']
      closed_nodes = step['closed']
      
      self.draw_grid()
      
      # mostrar nodos en lista abierta
      for pos in open_nodes:
        if pos != self.start and pos != self.goal:
          self.draw_cell(pos, "open")
      
      # mostrar nodos visitados 
      for pos in closed_nodes:
        if pos != self.start and pos != self.goal:
          self.draw_cell(pos, "closed")
      
      # destacar el nodo que se esta visitando actualmente
      if current_pos != self.start and current_pos != self.goal:
        self.draw_cell(current_pos, "visiting")
      
      # redibujar inicio y objetivo para que no se cubran 
      if self.start:
        self.draw_cell(self.start, 2)
      if self.goal:
        self.draw_cell(self.goal, 3)
      
      self.root.update()
      time.sleep(0.1)     # pausa para animación
    
    # mostrar camino final
    time.sleep(0.5)
    for pos in path:
      if pos != self.start and pos != self.goal:
        self.draw_cell(pos, "path")
        self.root.update()
        time.sleep(0.08)

  def draw_cell(self, pos, color_key):
    "Dibuja una celda individual"
    row, col = pos 
    x1 = col * self.cell_size
    y1 = row * self.cell_size
    x2 =  x1 + self.cell_size
    y2 =  y1 + self.cell_size
    
    color = self.colors[color_key] if isinstance(color_key, str) else self.colors[self.grid[row][col]]
    self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, outline="gray")
  
  def draw_grid(self):
    "Dibuja todo el grid"
    self.canvas.delete("all")
    
    for row in range(self.height):
      for col in range(self.width):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 =  x1 + self.cell_size
        y2 =  y1 + self.cell_size
        
        color = self.colors[self.grid[row][col]]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
  
  def clear_grid(self):
    "Limpia el grid"
    self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
    self.start = None
    self.goal = None
    self.mode = "obstacle"
    self.draw_grid()
    self.info_label.config(text="Grid reiniciado")
  
  def __call__(self):
    "Inicia la aplicación"
    self.root.mainloop()
  
#endregion

if __name__ == "__main__":
  # Crear y ejecutar el visualizador
  visualizer = AStar_Visualizer(
    h_function=manhattan_distance,
    cell_size=24,
    width=30,
    height=20
  )
  visualizer()
  