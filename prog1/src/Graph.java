import java.util.ArrayList;


public class Graph {
	
	private Vertex[] V;
	private ArrayList<Edge> E;
	
	public Graph(Vertex[] vertices, ArrayList<Edge> edges){
		V = vertices;
		E = edges;
	}
	
	public Vertex[] getV(){
		return V;
	}
	
	public ArrayList<Edge> getE(){
		return E;
	}

}
