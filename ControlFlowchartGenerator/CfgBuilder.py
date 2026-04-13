import graphviz

class CfgBuilder: 

    def __init__(self):
        self.dot = graphviz.Digraph(comment='Control Flow Graph')
    
    def createGraph(self, parsingResult):
        # Create Nodes
        for node in parsingResult:
            self.createNode(node["id"], node["content"], node["type"])

        print(self.dot)
        return self.dot


    def createNode(self, id, label, type=None):
        shape = self.getNodeStyle(type)
        self.dot.node(str(id), label=label, shape=shape)

    def createEdge(self, fromId, toId, label=""):
        self.dot.edge(str(fromId), str(toId), label=label)
    

    def getNodeStyle(self, style):

        match style:
            case "statement":
                return "rectangle"

            case "if_condition":
                return "diamond"
            
            case "end":
                return "ellipse"

            case _:
                raise Exception("Style: " + style + "not implemented")


    
        

