import java.util.ArrayList;


public class helloworld {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		// System.out.println("hello, joy!");
		
		/*ArrayList<Integer> testa = new ArrayList<Integer>();
		testa.add(2);
		testa.add(1);
		testa.add(4);
		testa.add(3);
		testa.add(6);
		testa.add(5);
		
		Heap h = new Heap();
		h.buildHeap(testa);
		for(int i = 0; i < h.size(); i++)
			System.out.println(h.get(i));
*/
	Generate(1, 5);
	Generate(2, 5);
	
	}
	
	public static double getDistance(double x1, double y1, double x2, double y2) {
		return Math.sqrt(Math.pow(x1-x2, 2.) + Math.pow(y1-y2, 2.));
	}
	
	public static void Generate(int type, int n) {
		
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
			V[i] = v;
		}
		
		for (int i = 0; i < n; i++){
			for (int j = i+1; j < n; j++){
				double w = 0.;
				if (type == 1){
					w = Math.random();
				}
				else if (type == 2){
//					double xi = V[i].getX();
//					double yi = V[i].getY();
//					double xj = V[j].getX();
//					double yj = V[j].getY();
//					System.out.println("xi: " + xi + " xj: " + xj + " yi: " + yi + " yj: " + yj);
					w = getDistance(V[i].getX(), V[i].getY(), V[j].getX(), V[j].getY());
				}
				Edge e = new Edge(V[i], V[j], w);
				E.add(e);
				System.out.println("i: " + i + " j: " + j + " w: " + w);
			}
		}
	}
	
	public void Prim() {
		int n = 5;
		int v = 0;
		int w = 0;
		int[] dist = new int[n];
		int[] prev = new int[n];
		ArrayList<Integer> s = new ArrayList<Integer>();
		ArrayList<Integer> ve = new ArrayList<Integer>();
		Heap h = new Heap();
	}
	
	

}
