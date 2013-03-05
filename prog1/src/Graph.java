import java.util.ArrayList;


public class Graph {
	
	private ArrayList<Vertex> V;
	private ArrayList<ArrayList<Edge>> E;
	
	public Graph(ArrayList<Vertex> vertices, ArrayList<ArrayList<Edge>> edges){
		V = vertices;
		E = edges;
	}
	
	public ArrayList<Vertex> getV(){
		return V;
	}
	
	public ArrayList<ArrayList<Edge>> getE(){
		return E;
	}
	
	public String toString(){
		String s = "Vertices: ";
		for(Vertex v : V){
			s += v + ", ";
		}
		s += "\n Edges: ";
//		for(Edge e : E){
//			s += e + ", ";
//		}
		
		return s;
	}

}
