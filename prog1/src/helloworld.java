import java.util.ArrayList;
import java.util.Arrays;


public class helloworld {

	public static void main(String[] args) {
		
		// parse args from command line input
		int n = Integer.parseInt(args[1]);
		int times = Integer.parseInt(args[2]);
		int type = Integer.parseInt(args[3]);

		// initialize avg array of all 0.'s
		double[] avg = new double[4];
		Arrays.fill(avg, 0.);
		
		double[] avg2 = new double[4];
		Arrays.fill(avg2, 0.);
		
		// for each time
		for (int i = 0; i < times; i++){
			// for each type of graph
			for (int t = 1; t < 5; t++) {
				// generate a graph of type t with n vertices
				Graph g = Generate(t, n);
				// store result vertex list from prim
				ArrayList<Vertex> res = Prim(g);
				
				// System.out.println(g.getV().get(0) == res.get(0));
				
				// sum up all distances in vertex list
				double dist = 0.;
				for (Vertex v: res)
					dist += v.getDist();
				// add onto array of averages
				avg[t - 1] += dist / times;
				
				double dist2 = 0.;
				// try adding up distances using prev pointers
				for (Vertex v: res){
					if (v.getPrev() != null){
						for (Edge e: g.getE()){
							if (e.getStart() == v.getPrev() && e.getEnd() == v) {
								dist2 += e.getWeight();
							}
						}
					}
				}
				avg2[t - 1] += dist2/times;
			}
		}
		
		// print out averages for each type of graph
		for (double a: avg)
			System.out.println(a);
		// output: average numpoints numtrials dimension
		//System.out.println(0 + " " + n + " " + times + " " + type);
		for (double a2: avg2)
			System.out.println(a2);
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
		
		ArrayList<Vertex> V = new ArrayList<Vertex>(n);
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
			V.add(v);
		}
		
		for (int i = 0; i < n; i++){
			for (int j = i+1; j < n; j++){
				double w = 0.;
				if (type == 1){
					w = Math.random();
				}
				else if (type == 2){
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i).getY(), V.get(j).getY());
				}
				else if (type == 3){
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i).getY(), V.get(j).getY(), V.get(i).getZ(), V.get(j).getZ());
				}
				else if (type == 4){
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i).getY(), V.get(j).getY(), V.get(i).getZ(), V.get(j).getZ(), V.get(i).getZZ(), V.get(j).getZZ());
				}
				Edge e = new Edge(V.get(i), V.get(j), w);
				E.add(e);
				//System.out.println("i: " + i + " j: " + j + " w: " + w);
			}
		}
		
		Graph g = new Graph(V, E);
		return g;
	}
	
	public static ArrayList<Vertex> Prim(Graph g) {
		// Get all vertices and edges of graph
		ArrayList<Vertex> V = g.getV();
		ArrayList<Edge> E = g.getE();
		// Initialize final set of vertices
		ArrayList<Vertex> S = new ArrayList<Vertex>();
		// Create heap for finding min distance at each point
		Heap h = new Heap();
		// Place on heap only starting vertex
		ArrayList<Vertex> start = new ArrayList<Vertex>();
		V.get(0).setDist(0);
		start.add(V.get(0));
		h.buildHeap(start);
		// Keep adding and taking off of heap
		while(h.size() > 0){
			// delete the minimum v, add v to S
			Vertex v = h.extractMin();
			// add v to the set S
			if(!S.contains(v)){
				S.add(v);
			}
			// for all the edges in E where the start point is v and the endpoint w is in V-S
			for(Edge e : E){
				if(e.getStart() == v && !S.contains(e.getEnd())){
					// if the dist of the endpoint is greater than the weight between the two points
					if(e.getEnd().getDist() > e.getWeight()){
						// set dist and prev of endpoint
						e.getEnd().setDist(e.getWeight());
						e.getEnd().setPrev(e.getStart());
						// add endpoint to heap
						h.insert(e.getEnd());
					}
				}
			}		
		}
		// return set of vertices with updated dist and weight
		return S;
	}
	
	

}
