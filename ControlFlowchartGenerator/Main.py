import ast
from Parser import CFGBuilder
from CfgBuilder import CfgDiagrammBuilder
import os
import platform

if platform.system() == "Windows":
    # Typische Installationspfade von Graphviz unter Windows
    possible_paths = [
        r"C:\Program Files\Graphviz\bin",
        r"C:\Program Files (x86)\Graphviz\bin",
        # Falls es über winget/choco installiert wurde, liegt es oft hier:
        os.path.expandvars(r"%LOCALAPPDATA%\bin\Graphviz\bin") 
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            os.environ["PATH"] += os.pathsep + path
            break

code = """
results = []
index = 0

while index < len(data):
    item = data[index]
    try:
        if item == 0:
            print("Null gefunden, überspringe...")
            index += 1
            continue  # Testet den Rücksprung zur While-Bedingung
        
        if item == "STOP":
            break     # Testet den Sprung aus der Schleife zum EXIT
            
        res = 10 / item
        results.append(res)
        
    except TypeError:
        print("Ungültiger Typ!")
        # Hier könnte man noch ein 'pass' oder Logik einbauen
        
    except ZeroDivisionError:
        print("Division durch Null!")
        
    finally:
        print(f"Verarbeite Index {index}")
        index += 1
        
return results
"""
tree = ast.parse(code)

parser = CFGBuilder()
nodes, edges = parser.build(tree) 

viz = CfgDiagrammBuilder()
graph = viz.createGraph(nodes, edges)

graph.render('kontrollfluss_diagramm', format='png', cleanup=True, view=True)