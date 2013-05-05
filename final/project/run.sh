#!/bin/bash
for i in {1..10}
do
	python run_game.py -d 0 >(tail -n 1 >> results.txt)
done