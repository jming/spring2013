import java.util.ArrayList;
import java.util.Arrays;


public class helloworld {

	public static void main(String[] args) {
		
		int n = Integer.parseInt(args[1]);
		int times = Integer.parseInt(args[2]);
		int type = Integer.parseInt(args[3]);
			
		//int n = 5;
		//int times = 5;
		double[] avg = new double[4];
		Arrays.fill(avg, 0.);
		
		for (int i = 0; i < times; i++){
			for (int t = 1; t < 5; t++) {
				Graph g = Generate(t, n);
				ArrayList<Vertex> res = Prim(g);
				double dist = 0.;
				for (Vertex v: res)
					dist += v.getDist();
				avg[t - 1] += dist / times;
			}
		}
		
		for (double a: avg)
			System.out.println(a);
		
//		Vertex v1 = new Vertex();
//		Vertex v2 = new Vertex();
//		Vertex v3 = new Vertex();
//		Vertex v4 = new Vertex();
//		
//		ArrayList<Vertex> vlist = new ArrayList<Vertex>();
//		vlist.add(v1);
//		vlist.add(v2);
//		vlist.add(v3);
//		vlist.add(v4);
//		
//		Edge e12 = new Edge(v1, v2, .1);
//		Edge e13 = new Edge(v1, v3, .5);
//		Edge e14 = new Edge(v1, v4, .1);
//		Edge e23 = new Edge(v2, v3, .4);
//		Edge e24 = new Edge(v2, v4, .1);
//		Edge e34 = new Edge(v3, v4, .3);
//		
//		ArrayList<Edge> elist = new ArrayList<Edge>();
//		elist.add(e12);
//		elist.add(e13);
//		elist.add(e14);
//		elist.add(e23);
//		elist.add(e24);
//		elist.add(e34);
//		
//		Graph test = new Graph(vlist, elist);
//		
//		ArrayList<Vertex> res = Prim(test);
//		
//		for (Vertex r: res)
//			System.out.println(r.getDist());
		

//		Graph one =	Generate(1, 2);
//		Graph two = Generate(2, 2);
//		Graph three = Generate(3, 2);
//		Graph four = Generate(4, 2);
//		
//		// Goal: Determine how expected average weight of minimum spanning three grows as a function of n
//		ArrayList<Vertex> eone = Prim(one);
//		System.out.println("size eone: " + eone.size());
//		ArrayList<Vertex> etwo = Prim(two);
//		System.out.println("size etwo: " + etwo.size());
//		ArrayList<Vertex> ethree = Prim(three);
//		System.out.println("size ethree: " + ethree.size());
//		ArrayList<Vertex> efour = Prim(four);
//		System.out.println("size efour: " + efour.size());
//		
//		System.out.println("eone \n");
//		for(Vertex v : eone){
//			System.out.println("x: " +v.getX() + "y: "+ v.getY() + "dist: " + v.getDist());
//		}
//		System.out.println("etwo \n");
//		for(Vertex v : etwo){
//			System.out.println("x: " +v.getX() + "y: "+ v.getY() + "dist: " + v.getDist());
//		}
//		System.out.println("etwo \n");
//		for(Vertex v : ethree){
//			System.out.println("x: " +v.getX() + "y: "+ v.getY() + "dist: " + v.getDist());
//		}
//		System.out.println("ethree \n");
//		for(Vertex v : efour){
//			System.out.println("x: " +v.getX() + "y: "+ v.getY() + "dist: " + v.getDist());
//		}
	
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
		ArrayList<Vertex> S = new ArrayList<Vertex>();
		//ArrayList<Integer> ve = new ArrayList<Integer>();
		Heap h = new Heap();
		ArrayList<Vertex> V = g.getV();
		ArrayList<Edge> E = g.getE();
//		for(Vertex ver: V){
//			System.out.println("vertices in graph: " + ver.getX() + ", " + ver.getY());
//		}
		// Build priority heap of vertices of Graph
		h.buildHeap(V);
		// set dist and prev for each vertex
		for(Vertex ve: V){
			ve.setDist(2);
			ve.setPrev(null);
		}
		//set distance of start vertex to 0
		V.get(0).setDist(0);
		//while the heap is nonempty
		//System.out.println("size heap: " + h.size());
		while(h.size() > 0){
			// delete the minimum v, add v to S
			Vertex v = h.extractMin();
			// add v to the set S
			if(!S.contains(v)){
				S.add(v);
				//System.out.println("S: " + S.get(0).getX()+ ", " + S.get(0).getY());
			}

			// for all the edges in E where the endpoint w is in V-S, do
			for(Edge e : E){
				if(S.contains(e.getEnd())){
					if(e.getEnd().getDist() > e.getWeight()){
						e.getEnd().setDist(e.getWeight());
						e.getEnd().setPrev(e.getStart());
						h.insert(e.getEnd());
					}
				}
			}		
		}
		return S;
	}
	
	

}
