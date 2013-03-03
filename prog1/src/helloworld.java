import java.util.ArrayList;


public class helloworld {

	public static void main(String[] args) {

	Graph one =	Generate(1, 5);
	Graph two = Generate(2, 5);
	Graph three = Generate(3, 5);
	Graph four = Generate(4, 5);
	
	// Goal: Determine how expected average weight of minimum spanning three grows as a function of n
	ArrayList<Edge> eone = Prim(one);
	
	}
	
	// TODO: Is there a better way to declare a method with optional args?
	public static double getDistance(double x1, double x2, double y1, double y2) {
		return Math.sqrt(Math.pow(x1-x2, 2.) + Math.pow(y1-y2, 2.));
	}
	
	public static double getDistance(double x1, double x2, double y1, double y2, double z1, double z2){
		return Math.sqrt(Math.pow(x1-x2, 2.) + Math.pow(y1-y2, 2.) + Math.pow(z1-z2, 2.));
	}
	
	public static double getDistance(double x1, double x2, double y1, double y2, double z1, double z2, double zz1, double zz2) {
		return Math.sqrt(Math.pow(x1-x2, 2.) + Math.pow(y1-y2, 2.) + Math.pow(z1-z2, 2.) + Math.pow(zz1-zz2, 2.));
	}
	
	// Generates graphs
	public static Graph Generate(int type, int n) {
		
		Vertex[] V = new Vertex[n];
		ArrayList<Edge> E = new ArrayList<Edge>();
		
		for (int i = 0; i < n; i++){
			Vertex v = null;
			if (type == 1){
				v = new Vertex();
			}
			else if (type == 2){
				v = new Vertex(Math.random(), Math.random());
			}
			else if (type == 3){
				v = new Vertex(Math.random(), Math.random(), Math.random());
			}
			else if (type == 4){
				v = new Vertex(Math.random(), Math.random(), Math.random(), Math.random());
			}
			V[i] = v;
		}
		
		for (int i = 0; i < n; i++){
			for (int j = i+1; j < n; j++){
				double w = 0.;
				if (type == 1){
					w = Math.random();
				}
				else if (type == 2){
					w = getDistance(V[i].getX(), V[j].getX(), V[i].getY(), V[j].getY());
				}
				else if (type == 3){
					w = getDistance(V[i].getX(), V[j].getX(), V[i].getY(), V[j].getY(), V[i].getZ(), V[j].getZ());
				}
				else if (type == 4){
					w = getDistance(V[i].getX(), V[j].getX(), V[i].getY(), V[j].getY(), V[i].getZ(), V[j].getZ(), V[i].getZZ(), V[j].getZZ());
				}
				Edge e = new Edge(V[i], V[j], w);
				E.add(e);
				System.out.println("i: " + i + " j: " + j + " w: " + w);
			}
		}
		
		Graph g = new Graph(V, E);
		return g;
	}
	
	public static ArrayList<Edge> Prim(Graph g) {
		int n = 5;
		int v = 0;
		int w = 0;
		int[] dist = new int[n];
		int[] prev = new int[n];
		ArrayList<Integer> s = new ArrayList<Integer>();
		//ArrayList<Integer> ve = new ArrayList<Integer>();
		Heap h = new Heap();
		// Build priority heap of vertices of Graph
		h.buildHeap(g.getV());
		// set dist and prev for each vertex
		for(Vertex v: g.getV()){
			dist[v] = 2;
			prev[v] = null;
		}
		//set distance of start vertex to 0
		dist[0] = 0;
		//while the heap is nonempty
			// delete the minimum v, add v to S
			// for all the edges in E where the endpoint w is in V-S, do
				// if dist[w] > length(v, w)
					// dist[w] = length(v, w); prev[w] = v; insert(w, dist[w], heap)
		
		return s;
	}
	
	

}
