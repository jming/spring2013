import java.util.*;

public class Heap {

	private ArrayList<Vertex> list;
	private int size;

	public Heap() {
		list = new ArrayList<Vertex>();
	}

	// swap the values in heap given two indices
	public void swap(int a, int b) {
		Vertex temp = list.get(a);
		list.set(a, list.get(b));
		list.set(b, temp);
	}
	
	// rearranges tree rooted at list.get(n) to be a minHeap
	public void minHeapify(int n){
		int l = left(n);
		int r = right(n);
		int smallest = 0;

		// set smallest
		if (l < list.size() && list.get(l).getDist() < list.get(n).getDist())
			smallest = l;
		else
			smallest = n;

		if (r < list.size()
				&& list.get(r).getDist() < list.get(smallest).getDist())
			smallest = r;

		// swap if necessary
		if (smallest != n) {
			swap(n, smallest);
			minHeapify(smallest);
		}

	}

	// Given an unordered list a, builds a max-heap
	public void buildHeap(ArrayList<Vertex> a) {
		list = a;
		size = a.size();
		for (int i = (int) Math.floor((double) a.size() / 2.0); i > 0; i--) {
			minHeapify(i);
		}
	}

	// given a non-empty heap returns top element and fixes the rest of the heap
	public Vertex extractMin() {
		Vertex min = list.remove(0);
		if (list.size() > 1) {
			minHeapify(0);
		}
		size--;
		return min;
	}

	// Adds value v into min-heap H
	public void insert(Vertex v) {
		if (list.contains(v)) {
			int in = list.indexOf(v);
			list.remove(in);
		}
		list.add(v);
		int n = list.size() - 1;
		while (n != 0 && list.get(parent(n)).getDist() > list.get(n).getDist()) {
			swap(parent(n), n);
			n = parent(n);
		}
		size++;
	}

	public int parent(int i){
		return (int) Math.floor(i/2.0);	
	}

	public int left(int i) {
		return 2 * i + 1;
	}

	public int right(int i) {
		return 2 * i + 2;
	}

	public int size() {
		return size;
	}

	public Vertex get(int i) {
		return list.get(i);
	}

	public ArrayList<Vertex> getList() {
		return list;
	}

}