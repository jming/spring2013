

public class Vertex {

	private int dist;
	private Vertex prev;
	private double x;
	private double y;
	private double z;
	private double zz;
	
	public Vertex(){
		dist = 2;
		prev = null;
	}
	
	public Vertex(double posx, double posy){
		x = posx;
		y = posy; 
		dist = 2;
		prev = null;
	}
	
	public Vertex(double posx, double posy, double posz) {
		x = posx;
		y = posy;
		z = posz;
		dist = 2;
		prev = null;
	}
	
	public Vertex(double posx, double posy, double posz, double poszz){
		x = posx;
		y = posy;
		z = posz;
		zz = poszz;
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
	
	public double getZ(){
		return z;
	}
	
	public double getZZ(){
		return zz;
	}
}