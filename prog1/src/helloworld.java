import java.util.ArrayList;
import java.util.Arrays;

public class helloworld {

	public static void main(String[] args) {

		// parse args from command line input
		int n = Integer.parseInt(args[1]);
		int times = Integer.parseInt(args[2]);
		// int type = Integer.parseInt(args[3]);

		// initialize avg array of all 0.'s
		int t = 1;
		// for each time
		Graph g = Generate(t, n);
		// store result vertex list from prim
		ArrayList<Vertex> res = Prim(g);

		// ADD UP DISTANCES IN VERTEX LIST

		// sum up all distances in vertex list
		double dist = 0.;
		for (Vertex v : res) {
			dist += v.getDist();
			System.out.println(v);
		}
		// add onto array of averages
		System.out.println("Result: " + dist);
		

	}

	// TODO: Is there a better way to declare a method with optional args?
	public static double getDistance(double x1, double x2, double y1, double y2) {
		return Math.sqrt(Math.pow(x1 - x2, 2.) + Math.pow(y1 - y2, 2.));
	}

	public static double getDistance(double x1, double x2, double y1,
			double y2, double z1, double z2) {
		return Math.sqrt(Math.pow(x1 - x2, 2.) + Math.pow(y1 - y2, 2.)
				+ Math.pow(z1 - z2, 2.));
	}

	public static double getDistance(double x1, double x2, double y1,
			double y2, double z1, double z2, double zz1, double zz2) {
		return Math.sqrt(Math.pow(x1 - x2, 2.) + Math.pow(y1 - y2, 2.)
				+ Math.pow(z1 - z2, 2.) + Math.pow(zz1 - zz2, 2.));
	}

	// Generates graphs
	public static Graph Generate(int type, int n) {

		ArrayList<Vertex> V = new ArrayList<Vertex>(n);
		ArrayList<Edge> E = new ArrayList<Edge>();

		for (int i = 0; i < n; i++) {
			Vertex v = null;
			if (type == 1) {
				v = new Vertex();
			} else if (type == 2) {
				v = new Vertex(Math.random(), Math.random());
			} else if (type == 3) {
				v = new Vertex(Math.random(), Math.random(), Math.random());
			} else if (type == 4) {
				v = new Vertex(Math.random(), Math.random(), Math.random(),
						Math.random());
			}
			V.add(v);
		}

		for (int i = 0; i < n; i++) {
			for (int j = i + 1; j < n; j++) {
				double w = 0.;
				if (type == 1) {
					w = Math.random();
				} else if (type == 2) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY());
				} else if (type == 3) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY(), V.get(i).getZ(), V.get(j)
							.getZ());
				} else if (type == 4) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY(), V.get(i).getZ(), V.get(j)
							.getZ(), V.get(i).getZZ(), V.get(j).getZZ());
				}
				Edge e = new Edge(V.get(i), V.get(j), w);
				E.add(e);
			}
		}

		Graph g = new Graph(V, E);
		return g;
	}

	public static ArrayList<Vertex> Prim(Graph g) {

		// Get all vertices and edges of graph
		ArrayList<Vertex> V = g.getV();
		ArrayList<Edge> E = g.getE();
		System.out.println("E: ");
		for (Edge e: E){
			System.out.println(e);
		}
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
		while (h.size() > 0) {
			System.out.println("H: ");
			for (Vertex i: h.getList()) {
				System.out.println("v: " +i);
			}
			// delete the minimum v, add v to S
			Vertex v = h.extractMin();
			
			// add v to the set S
			if (!S.contains(v)) {
				S.add(v);
			}

			System.out.println("S: ");
			for (Vertex s: S){
				System.out.println("s: " + s);
			}
			// for all the edges in E where the start/end is v and the other is in V-S
			for (Edge e : E) {
				Vertex v1 = null;

				if (e.getStart() == v && !S.contains(e.getEnd())) {
					v1 = e.getEnd();
				} else if (e.getEnd() == v && !S.contains(e.getStart())) {
					v1 = e.getStart();
				}
				System.out.println("v1: " + v1);
				if (v1 != null && v1.getDist() > e.getWeight()) {
					v1.setDist(e.getWeight());
					v1.setPrev(v);
					h.insert(v1);
				}
			}
		}
		// return set of vertices with updated dist and weight
		return S;
	}

}
