import java.util.ArrayList;
import java.lang.System;

public class randmst {

	public static void main(String[] args) {

		// parse args from command line input
		int n = Integer.parseInt(args[1]);
		int times = Integer.parseInt(args[2]);
		int type = Integer.parseInt(args[3]);

		double result = 0.;

		// for each time
		for (int i = 0; i < times; i++) {

			// generate a graph of type with n vertices
			Graph g = Generate(type, n);
			// store result vertex list from prim
			ArrayList<Vertex> res = Prim(g);

			double dist = 0.;
			// sum up all distances in vertex list
			for (Vertex v : res) {
				dist += v.getDist();
			}

			result += dist / times;
		}

		// output average numvertex numtrials type
		System.out.println(result + " " + n + " " + times + " " + type);

	}

	// Finding distance between two points in given dimensions
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

		// Creates an empty list of vertices and edges
		ArrayList<Vertex> V = new ArrayList<Vertex>(n);
		ArrayList<ArrayList<Edge>> E = new ArrayList<ArrayList<Edge>>();

		// create all edges less than i
		for (int i = 0; i < n; i++) {
			// create vertex with proper dimensions
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
		
		//int temporary_counter = 0;

		for (int i = 0; i < n; i++) {
			// create list of edges emitting from given vertex
			ArrayList<Edge> tmp = new ArrayList<Edge>();
			int j = i + 1;
			while (j < n){
				double w = 0.;
				boolean add = false;
				// calculate weight based on type
				if (type == 1) {
					w = Math.random();
					add = (w < 3 * Math.pow(n, -0.9));
				} else if (type == 2) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY());
					add = (w < 1.8 * Math.pow(n, -0.5));
				} else if (type == 3) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY(), V.get(i).getZ(), V.get(j)
							.getZ());
					add = (w < 1.8 * Math.pow(n, -0.35));
				} else if (type == 4) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY(), V.get(i).getZ(), V.get(j)
							.getZ(), V.get(i).getZZ(), V.get(j).getZZ());
					add = (w < 1.6 * Math.pow(n, -.27));
				}
				// add into list of edges
				if (add) {
					//System.out.println(j);
					Edge e = new Edge(V.get(i), V.get(j), w);
					tmp.add(e);
					//temporary_counter++;
				}
				j++;
			}
			// add temp list to edge list
			E.add(tmp);
		}

		// return new graph
		Graph g = new Graph(V, E, type);
		return g;
	}

	public static ArrayList<Vertex> Prim(Graph g) {

		// Get all vertices and edges of graph
		ArrayList<Vertex> V = g.getV();
		ArrayList<ArrayList<Edge>> E = g.getE();
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
		while (h.getList().size() > 0) {

			// delete the minimum v, add v to S
			Vertex v = h.extractMin();

			// add v to the set S
			if (!S.contains(v)) {
				S.add(v);
			}

			// for all the edges in E where the start/end is v and the other !S
			for (ArrayList<Edge> L : E) {
				for (Edge e : L) {

					Vertex v1 = null;

					// find vertex sharing edge
					if (e.getStart() == v && !S.contains(e.getEnd())) {
						v1 = e.getEnd();
					} else if (e.getEnd() == v && !S.contains(e.getStart())) {
						v1 = e.getStart();
					}
					// update dist, insert into heap
					if (v1 != null && v1.getDist() > e.getWeight()) {
						v1.setDist(e.getWeight());
						v1.setPrev(v);
						h.insert(v1);
					}
				}
			}
		}
		// return set of vertices with updated dist and weight
		return S;
	}

}
