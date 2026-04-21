import ast
from typing import List, Tuple, Optional


class CFGNode:
    _id_counter = 0

    def __init__(self, label: str):
        self.id = CFGNode._id_counter
        CFGNode._id_counter += 1
        self.label = label

    def __repr__(self):
        return f"Node({self.id}: {self.label})"

class CFGBuilder(ast.NodeVisitor):

    def __init__(self):
        self.nodes: List[CFGNode] = []
        self.edges: List[Tuple[CFGNode, CFGNode]] = []

        self.current: Optional[CFGNode] = None
        self.loop_stack: List[CFGNode] = []  # for break/continue targets

    def new_node(self, label: str) -> CFGNode:
        node = CFGNode(label)
        self.nodes.append(node)
        return node

    def connect(self, src: Optional[CFGNode], dst: CFGNode):
        if src is not None:
            self.edges.append((src, dst))

    
    # entry
    def build(self, tree: ast.AST):
        entry = self.new_node("ENTRY")
        self.current = entry

        self.visit(tree)

        exit_node = self.new_node("EXIT")
        self.connect(self.current, exit_node)

        return self.nodes, self.edges
    

    def visit_Module(self, node: ast.Module):
        for stmt in node.body:
            self.visit(stmt)

    

    def generic_statement(self, node, label):
        stmt_node = self.new_node(label)
        self.connect(self.current, stmt_node)
        self.current = stmt_node

    def visit_Assign(self, node: ast.Assign):
        self.generic_statement(node, "Assign")

    def visit_Expr(self, node: ast.Expr):
        self.generic_statement(node, "Expr")

    def visit_Return(self, node: ast.Return):
        return_node = self.new_node("Return")
        self.connect(self.current, return_node)
        self.current = None  # Return beendet den Kontrollfluss

    # ---------- IF ----------

    def visit_If(self, node: ast.If):
        if_node = self.new_node("If")
        self.connect(self.current, if_node)

        # THEN
        self.current = if_node
        for stmt in node.body:
            self.visit(stmt)
        then_end = self.current

        # ELSE
        self.current = if_node
        for stmt in node.orelse:
            self.visit(stmt)
        else_end = self.current

        # MERGE
        merge = self.new_node("Merge")

        if then_end:
            self.connect(then_end, merge)
        if else_end:
            self.connect(else_end, merge)

        self.current = merge

    # ---------- WHILE ----------

    def visit_While(self, node: ast.While):
        while_node = self.new_node("While")
        self.connect(self.current, while_node)

        loop_exit = self.new_node("LoopExit")
        self.loop_stack.append(loop_exit)

        # Body
        self.current = while_node
        for stmt in node.body:
            self.visit(stmt)

        # Rückkante
        if self.current:
            self.connect(self.current, while_node)

        # False-Kante
        self.connect(while_node, loop_exit)

        self.loop_stack.pop()
        self.current = loop_exit

    
    def visit_For(self, node: ast.For):
        for_node = self.new_node("For")
        self.connect(self.current, for_node)

        # Exit-Knoten für break
        loop_exit = self.new_node("ForExit")
        self.loop_stack.append(loop_exit)

        # Schleifenrumpf
        self.current = for_node
        for stmt in node.body:
            self.visit(stmt)

        # Rückkante (nächste Iteration)
        if self.current:
            self.connect(self.current, for_node)

        # Schleife verlassen
        self.connect(for_node, loop_exit)

        self.loop_stack.pop()
        self.current = loop_exit


    # ---------- BREAK / CONTINUE ----------

    def visit_Break(self, node: ast.Break):
        break_node = self.new_node("Break")
        self.connect(self.current, break_node)
        self.connect(break_node, self.loop_stack[-1])
        self.current = None

    def visit_Continue(self, node: ast.Continue):
        continue_node = self.new_node("Continue")
        self.connect(self.current, continue_node)
        self.connect(continue_node, self.loop_stack[-1])
        self.current = None

    def visit_Try(self, node: ast.Try):
        try_node = self.new_node("Try")
        self.connect(self.current, try_node)

        finally_node = self.new_node("Finally")

       # try block
        self.current = try_node
        for stmt in node.body:
            self.visit(stmt)

        normal_end = self.current
        if normal_end:
            self.connect(normal_end, finally_node)

       # except block
        for handler in node.handlers:
            except_node = self.new_node("Except")
            self.connect(try_node, except_node)

            self.current = except_node
            for stmt in handler.body:
                self.visit(stmt)

            except_end = self.current
            if except_end:
                self.connect(except_end, finally_node)

       #finally block
        self.current = finally_node
        for stmt in node.finalbody:
            self.visit(stmt)

        #continue after finally
        self.current = finally_node