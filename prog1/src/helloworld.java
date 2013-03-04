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
		// output: average numpoints numtrials dimension
		//System.out.println(0 + " " + n + " " + times + " " + type);
	
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
