

public class Vertex {

	private int dist;
//	private int name;
	private Vertex prev;
	private double x;
	private double y;
	
	public Vertex(){
//		name = n;
		dist = 2;
		prev = null;
	}
	
	public Vertex(double posx, double posy){
		x = posx;
		y = posy; 
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
	
	public double getX(){
		return x;
	}
	
	public double getY(){
		return y;
	}
	
//	public int getName(){
//		return name;
//	}
}
