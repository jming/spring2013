def main():

	f = open('poisnous.txt')
	contents = f.readlines()
	f.close

	new_contents = []
	for line in contents:
		if not line.strip():
			continue
		else: 
			new_contents.append(line)

	fp = open('poisnous.txt')
main()