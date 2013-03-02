import java.util.*;

public class Heap {
	
	private ArrayList<Integer> list;

	public Heap(){
		list = new ArrayList<Integer>();	
	}
	
	// swap the values in heap given two indices
	public void swap(int a, int b){
		int temp = list.get(a);
		list.set(a, list.get(b));
		list.set(b, temp);
	}
	
	// rearranges tree rooted at list.get(n) to be a maxHeap
	public void minHeapify(int n){
		
		// initialize variables
		int l = left(list.indexOf(n));
		int r = right(list.indexOf(n));
		int smallest = 0;
		
		// set largest
		if (l < list.size() && list.get(l) < list.get(n))
			smallest = l;
		else
			smallest = n;
		
		if (r < list.size() && list.get(r) < list.get(smallest))
			smallest = r;
		
		// swap if necessary
		if (smallest != n) {
			swap(n, smallest);
			minHeapify(smallest);
		}
		
	}
	
	// Given an unordered list a, builds a max-heap
	public void buildHeap(ArrayList<int[]> a){
		for(int i = (int) Math.floor((double) a.size()/2.0); i > 0; i--)
		{
			minHeapify(i);
		}
	}
	
	public void extractMax(){
		
	}
	
	public void insert(int v){
		
	}
	

	public int parent(int i){
		return (int) Math.floor(i/2.0);	
	}
	
	public int left(int i){
		return 2*i;
	}

	public int right(int i){
		return 2*i + 1;
	}
	

}
