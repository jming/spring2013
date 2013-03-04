import java.util.ArrayList;
import java.util.Arrays;


public class helloworld {

	public static void main(String[] args) {
		
		Vertex v1 = new Vertex();
		Vertex v2 = new Vertex();
		Vertex v3 = new Vertex();
		Vertex v4 = new Vertex();
		
		ArrayList<Vertex> vlist = new ArrayList<Vertex>();
		vlist.add(v1);
		vlist.add(v2);
		vlist.add(v3);
		vlist.add(v4);

		Edge e12 = new Edge(v1, v2, .7);
		Edge e13 = new Edge(v1, v3, .2);
		Edge e14 = new Edge(v1, v4, .3);
		Edge e23 = new Edge(v2, v3, .5);
		Edge e24 = new Edge(v2, v4, .1);
		Edge e34 = new Edge(v3, v4, .5);

		ArrayList<Edge> elist = new ArrayList<Edge>();
		elist.add(e12);
		elist.add(e13);
		elist.add(e14);
		elist.add(e23);
		elist.add(e24);
		elist.add(e34);

		Graph test = new Graph(vlist, elist);

		ArrayList<Vertex> res = Prim(test);

		System.out.println("getDist: ");
		for (Vertex r: res)
			System.out.println(r.getDist());
		
		System.out.println("getPrev: ");
		for (Vertex v: res){
			System.out.println("v: " + v);
			// find the weight between 2 vertices
			if (v.getPrev() != null){
				// really stupid way to get the edge between 2 vertices
				for (Edge e: test.getE()){
					if (e.getStart() == v.getPrev() && e.getEnd() == v) {
						System.out.println(e.getWeight());
					} else if (e.getEnd() == v.getPrev() && e.getStart() == v) 
						System.out.println(e.getWeight());
				}
			}
		}
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
			// for all the edges in E where the startpoint or endpoint is v and the other point is in V-S
			for(Edge e : E){
//				Vertex a = null;
//				Vertex b = null;
				Vertex v1 = null;
				
				if (e.getStart() == v && !S.contains(e.getEnd())) {
					v1 = e.getEnd();
				}
				else if (e.getEnd() == v && !S.contains(e.getStart())) {
					v1 = e.getStart();
				}
//				
//				if (e.getStart() == v && !S.contains(e.getEnd())) {
//					a = v;
//					b = e.getEnd();
//				}
//				else if (e.getEnd() == v && !S.contains(e.getStart())) {
//					a = e.getStart();
//					b = v;
//				}
//				if (a != null && b != null & b.getDist() > e.getWeight()) {
//					b.setDist(e.getWeight());
//					b.setPrev(a);
//					h.insert(b);
//				}
				if (v1!=null && v1.getDist() > e.getWeight()) {
					v1.setDist(e.getWeight());
					v1.setPrev(v);
					h.insert(v1);
				}
//				if ((e.getStart() == v && !S.contains(e.getEnd())) || 
//						(e.getEnd() == v && !S.contains(e.getStart()))) {
//					// if the dist of the endpoint is greater than the weight between the two points
//					if(e.getEnd().getDist() > e.getWeight()){
//						// set dist and prev of endpoint
//						e.getEnd().setDist(e.getWeight());
//						e.getEnd().setPrev(e.getStart());
//						// add endpoint to heap
//						h.insert(e.getEnd());
//					}
//				}
			}
			System.out.println("H: ");
			for (Vertex i: h.getList()){
				System.out.println("v: " + i);
			}
			System.out.println("S: ");
			for (Vertex s: S){
				System.out.println("s: " + s);
			}
		}
		// return set of vertices with updated dist and weight
		return S;
	}
	
	

}
