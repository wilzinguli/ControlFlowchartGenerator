import graphviz

class CfgDiagrammBuilder: 
    """
    Diese Klasse nimmt die logischen Daten (Nodes und Edges) vom Parser entgegen
    und transformiert sie in eine grafische Darstellung mittels Graphviz.
    """

    def __init__(self):
        self.dot = graphviz.Digraph(comment='Control Flow Graph', engine='dot')
        self.dot.attr(nodesep='0.5', ranksep='0.5')
        self.dot.attr('node', fontname='Arial', fontsize='10')

    def createGraph(self, nodes, edges):
        """
        :param nodes: Liste von CFGNode-Objekten (aus Parser.py)
        :param edges: Liste von Tupeln (src_node, dst_node) (aus Parser.py)
        """
        # 1. Alle Knoten zeichnen
        for node in nodes:
            shape = self._determine_shape(node.label)
            color = self._determine_color(node.label)
            
            self.dot.node(
                name=str(node.id), 
                label=node.label, 
                shape=shape, 
                style='filled', 
                fillcolor=color
            )

        for src_node, dst_node in edges:
            # Da src_node und dst_node Objekte sind, greifen wir auf deren IDs zu
            self.dot.edge(str(src_node.id), str(dst_node.id))

        return self.dot

    def _determine_shape(self, label):
        label_lower = label.lower()
        
        if any(x in label_lower for x in ["if", "while", "for", "try", "match", "except"]):
            return "diamond"
        
        elif any(x in label_lower for x in ["entry", "exit", "return", "break", "continue"]):
            return "ellipse"
        
        else:
            return "rectangle"

    def _determine_color(self, label):
        label_lower = label.lower()
        if "entry" in label_lower: return "#CFFFCE" 
        if "exit" in label_lower: return "#FFCECE"  
        if any(x in label_lower for x in ["if", "while", "for"]): return "#FFF4CE" 
        return "#F5F5F5"