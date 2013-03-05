import java.util.ArrayList;
<<<<<<< HEAD
import java.util.Arrays;
import java.lang.System;

// import java.util.PriorityQueue;

public class randmst {

	public static void main(String[] args) {
		
		long start = System.currentTimeMillis();
=======
import java.lang.System;

public class randmst {

	public static void main(String[] args) {
>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab

		// parse args from command line input
		int n = Integer.parseInt(args[1]);
		int times = Integer.parseInt(args[2]);
<<<<<<< HEAD
		// int type = Integer.parseInt(args[3]);

		// initialize avg array of all 0.'s
		double[] avg = new double[4];
		Arrays.fill(avg, 0.);

		double[] avg2 = new double[4];
		Arrays.fill(avg2, 0.);
		double[] max = new double[4];
		Arrays.fill(max, 0.);
		
		// for each time
		for (int i = 0; i < times; i++) {
			// for each type of graph
			for (int t = 1; t < 5; t++) {
				// generate a graph of type t with n vertices
				Graph g = Generate(t, n);
				// store result vertex list from prim
				ArrayList<Vertex> res = Prim(g);

				// ADD UP DISTANCES IN VERTEX LIST

				// sum up all distances in vertex list
				double dist = 0.;
				for (Vertex v : res){
					if (v.getDist() > max[t -1])
						max[t - 1] = v.getDist();
					dist += v.getDist();
				}
				// add onto array of averages
				avg[t - 1] += dist / times;

				// ADD UP DISTANCES USING PREV POINTERS
				double dist2 = 0.;
				// for each vertex
				for (Vertex v : res) {
					// find the weight between 2 vertices
					if (v.getPrev() != null) {
						// really stupid way to get the edge between 2 vertices
						for (Edge e : g.getE()) {
							// need to account for prev pointing forward (incr)
							// and backward (decr)
							if ((e.getStart() == v.getPrev() && e.getEnd() == v)
									|| (e.getEnd() == v.getPrev() && e
											.getStart() == v)) {
								dist2 += e.getWeight();
							}
						}
					}
				}
				// add onto array of averages
				avg2[t - 1] += dist2 / times;
			}
		}
		long end = System.currentTimeMillis();

		// print out averages for each type of graph

		System.out.println("getDist: ");
		for (double a : avg){
			System.out.println(a);
		}
		System.out.println("getPrev: ");
		for (double a2 : avg2)
			System.out.println(a2);
		
		System.out.println("total runtime: " + (end - start));
		
		System.out.println("longest edge in MST: ");
		for (double m : max)
			System.out.println(m);
	}

	// TODO: Is there a better way to declare a method with optional args?
=======
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
>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
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

<<<<<<< HEAD
		ArrayList<Vertex> V = new ArrayList<Vertex>(n);
		ArrayList<Edge> E = new ArrayList<Edge>();

		for (int i = 0; i < n; i++) {
=======
		// Creates an empty list of vertices and edges
		ArrayList<Vertex> V = new ArrayList<Vertex>(n);
		ArrayList<ArrayList<Edge>> E = new ArrayList<ArrayList<Edge>>();

		// create all edges less than i
		for (int i = 0; i < n; i++) {
			// create vertex with proper dimensions
>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
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
<<<<<<< HEAD
=======
			// add to vertex list
>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
			V.add(v);
		}

		for (int i = 0; i < n; i++) {
<<<<<<< HEAD
			for (int j = i + 1; j < n; j++) {
				double w = 0.;
				boolean add = false;
				if (type == 1) {
					w = Math.random();
					add = (w < 0.3334);
				} else if (type == 2) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY());
					add = (w < 0.5215);
=======
			// create list of edges emitting from given vertex
			ArrayList<Edge> tmp = new ArrayList<Edge>();
			int j = i + 1;
			while (j < n && tmp.size() < 30){
				double w = 0.;
				boolean add = false;
				// calculate weight based on type
				if (type == 1) {
					w = Math.random();
					add = (w < 4.0351 * Math.pow(n, -0.214));
				} else if (type == 2) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY());
					add = (w < 2.4661 * Math.pow(n, -0.448));
>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
				} else if (type == 3) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY(), V.get(i).getZ(), V.get(j)
							.getZ());
<<<<<<< HEAD
					add = (w < 0.6618);
=======
					add = (w < 1.6227 * Math.pow(n, -0.268));
>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
				} else if (type == 4) {
					w = getDistance(V.get(i).getX(), V.get(j).getX(), V.get(i)
							.getY(), V.get(j).getY(), V.get(i).getZ(), V.get(j)
							.getZ(), V.get(i).getZZ(), V.get(j).getZZ());
<<<<<<< HEAD
					add = (w < 0.7777);
				}
				//if (add) {
					Edge e = new Edge(V.get(i), V.get(j), w);
					E.add(e);
				//}
			}
		}

=======
					add = (w < 1.5783 * Math.pow(n, -.0214));
				}
				// add into list of edges
				if (add) {
					Edge e = new Edge(V.get(i), V.get(j), w);
					tmp.add(e);
				}
				j++;
			}
			// add temp list to edge list
			E.add(tmp);
		}

		// return new graph
>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
		Graph g = new Graph(V, E);
		return g;
	}

	public static ArrayList<Vertex> Prim(Graph g) {

		// Get all vertices and edges of graph
		ArrayList<Vertex> V = g.getV();
<<<<<<< HEAD
		ArrayList<Edge> E = g.getE();
		// System.out.println("E: ");
		// for (Edge e : E) {
		// System.out.println(e);
		// }
=======
		ArrayList<ArrayList<Edge>> E = g.getE();

>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
		// Initialize final set of vertices
		ArrayList<Vertex> S = new ArrayList<Vertex>();

		// Create heap for finding min distance at each point
		Heap h = new Heap();
<<<<<<< HEAD
		// PriorityQueue<Vertex> queue = new PriorityQueue<Vertex>(V);
=======

>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
		// Place on heap only starting vertex
		ArrayList<Vertex> start = new ArrayList<Vertex>();
		V.get(0).setDist(0);
		start.add(V.get(0));
		h.buildHeap(start);

		// Keep adding and taking off of heap
		while (h.getList().size() > 0) {
<<<<<<< HEAD
			// // System.out.println("hsize: " + h.getLsize());
			// System.out.println("H: ");
			// for (Vertex i : h.getList()) {
			// System.out.println("v: " + i);
			// }
			// delete the minimum v, add v to S
			Vertex v = h.extractMin();
			// Vertex v = queue.peek();
			// queue.remove(v);
=======

			// delete the minimum v, add v to S
			Vertex v = h.extractMin();

>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
			// add v to the set S
			if (!S.contains(v)) {
				S.add(v);
			}

<<<<<<< HEAD
			// System.out.println("S: ");
			// for (Vertex s : S) {
			// System.out.println("s: " + s);
			// }
			// for all the edges in E where the start/end is v and the other is
			// in V-S
			for (Edge e : E) {
				Vertex v1 = null;

				if (e.getStart() == v && !S.contains(e.getEnd())) {
					v1 = e.getEnd();
				} else if (e.getEnd() == v && !S.contains(e.getStart())) {
					v1 = e.getStart();
				}
				// System.out.println("v1: " + v1);
				if (v1 != null && v1.getDist() > e.getWeight()) {
					v1.setDist(e.getWeight());
					v1.setPrev(v);
					h.insert(v1);
					// queue.add(v1);
=======
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
>>>>>>> b369259fe7d48a1667f09be8591243d1ece172ab
				}
			}
		}
		// return set of vertices with updated dist and weight
		return S;
	}

}
