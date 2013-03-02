import java.util.ArrayList;


public class helloworld {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("hello, joy!");
		
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
	
	}
	
	public static void Generate(int type, int n) {
		Vertex[] V = new Vertex[n];
		ArrayList<Edge> E = new ArrayList<Edge>();
		
		for (int i = 0; i < n; i++){
			Vertex v = new Vertex();
			V[i] = v;
		}
		for (int i = 0; i < n; i++){
			for (int j = i+1; j <n; j++){
				// TODO: Randomize w's
				int w = 0;
				Edge e = new Edge(V[i], V[j], w);
				E.add(e);
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
