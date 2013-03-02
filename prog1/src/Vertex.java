

public class Vertex {

	private int dist;
	private int name;
	private Vertex prev;
	
	public Vertex(int n){
		name = n;
		dist = 2;
		prev = null;
	}
	
	public void setPrev(Vertex v){
		prev = v;
	}
	
	public void setDist(int d){
		dist = d;
	}
	
	public int getDist(){
		return dist;
	}
	
	public Vertex getPrev(){
		return prev;
	}
	
	public int getName(){
		return name;
	}
}
