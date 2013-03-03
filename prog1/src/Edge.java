
public class Edge {
	
	private Vertex u;
	private Vertex v;
	private double w;
	
	public Edge(Vertex start, Vertex end, double weight){
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
	
	public double getWeight(){
		return w;
	}

}
