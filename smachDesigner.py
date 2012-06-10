#!/usr/bin/python

# http://qt-project.org/doc/qt-4.8/graphicsview-elasticnodes.html
# http://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/examples/graphicsview/elasticnodes.py
# http://www.youtube.com/watch?v=I0n07iuowvY
# http://www.diotavelli.net/PyQtWiki/PyQt4Examples
# http://doc.trolltech.com/4.3/graphicsview-elasticnodes.html



import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Edge(QGraphicsItem):
    Type = QGraphicsItem.UserType + 2
    
    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()
        
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        
    def type(self):
        return Edge.Type
        
    def paint(self, painter, option, widget):
        print "ho"
        line = QLineF(self.mapFromItem(self.source, 0,0),
                      self.mapFromItem(self.dest, 0,0))
        painter.drawLine(line)
    
  
        
    def boundingRect(self):
        self.sourcePoint = self.mapFromItem(self.source,0,0)
        self.destPoint = self.mapFromItem(self.dest,0,0)
        return QRectF(-200,-200,800,800)
        # return QRectF(self.sourcePoint, QSizeF(self.destPoint.x() - self.sourcePoint.x(),
        #                                   self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-25,-25,25,25)

class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1
    
    def __init__(self, graphWidget):
        print "nodeInit"
        super(Node, self).__init__()
        
        self.graph = graphWidget
        self.edgeList = []
        #self.setZValue(10)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
    def type(self):
        return Node.Type
    
    def addEdge(self, edge):
        self.edgeList.append(edge)
    
    def boundingRect(self):
        return QRectF(-15,-15,25,25)
        
    def paint(self, painter, option, widget):
        print "hi"
        painter.setBrush(Qt.darkGray)
        painter.setPen(QPen(Qt.black, 0))
        if self == self.graph.fromNode:
            painter.setPen(QPen(Qt.red, 1))
        painter.drawEllipse(-10,-10,20,20)
        print self.edgeList        
    
    def itemChange(self, change, value):
        #if change == QGraphicsItem.ItemPositionChange:
        self.update()
        for edge in self.edgeList:
            edge.update(-200,-200,500,500)
                
        return super(Node, self).itemChange(change, value) 
    
    def mousePressEvent(self, event):
        if QApplication.mouseButtons() == Qt.RightButton:
            if self.graph.fromNode is None:
                print "yup"
                self.graph.fromNode = self
                print self.graph.fromNode
                print "selfgraph"
            else:
                print "yep"
                edge1 = Edge(self.graph.fromNode, self)
                self.graph.scene.addItem(edge1)
                self.edgeList.append(edge1)
                self.graph.fromNode.edgeList.append(edge1)
                self.graph.fromNode = None
        self.update()
        for edge in self.edgeList:
            edge.update(-200,-200,500,500)
        #self.setSelected(True)
        #super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        for edge in self.edgeList:
            edge.update(-200,-200,500,500)
        super(Node, self).mouseReleaseEvent(event)


        
class GraphWidget(QGraphicsView):
    def __init__(self):
        super(GraphWidget, self).__init__()
        
        self.fromNode = None
        
        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        
        node1 = Node(self)
        self.scene.addItem(node1)
        node2 = Node(self)
        self.scene.addItem(node2)
        self.scene.addItem(Edge(node1, node2))
        node1.setPos(10,10)
        node2.setPos(30,40)
        
        #ll = QGraphicsLineItem(0,0,0,100)
        #scene.addItem(ll)
        
        self.setMinimumSize(400,400)
        self.setWindowTitle("smachDesigner")
        
    def mousePressEvent(self, event):
        ###todo: implement line drawing here! self.fromNode + self.scene.selectedItems (if right button)
        print "here:"
        print self.fromNode
        if QApplication.mouseButtons() == Qt.MiddleButton:
            node = Node(self)
            self.scene.addItem(node)
            node.setPos( self.mapToScene(self.mapFromGlobal(QCursor.pos())) )
            print "mouse!"
        if QApplication.mouseButtons() == Qt.RightButton:
            self.fromNode = None
        super(GraphWidget, self).mousePressEvent(event)

app = QApplication(sys.argv)
widget = GraphWidget()
widget.show()

sys.exit(app.exec_())
