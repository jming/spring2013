import java.util.ArrayList;


public class helloworld {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("hello, joy!");
		
		ArrayList<Integer> testa = new ArrayList<Integer>();
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

	}

}
