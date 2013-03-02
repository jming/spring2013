
public class Edge {
	
	private Vertex u;
	private Vertex v;
	private int w;
	
	public Edge(Vertex start, Vertex end, int weight){
		u = start;
		v = end;
		w = weight;
	}
	
	public Vertex getStart(){
		return u;
	}
	
	public Vertex getEnd(){
		return v;
	}
	
	public int getWeight(){
		return w;
	}

}
