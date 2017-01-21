init:
	pip3 install -r requirements.txt
	if [ ! -d "data" ]; then mkdir data; fi
test:
	pytest
