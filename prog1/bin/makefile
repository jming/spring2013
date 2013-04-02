JFLAGS = -g
JC = javac
.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
	Edge.java \
	Graph.java \
	Heap.java \
	randmst.java \
	Vertex.java

default: classes

classes: $(CLASSES:.java=.class)

clean:
	$(RM) *.class