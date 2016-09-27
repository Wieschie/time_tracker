init:
	pip3 install -r requirements.txt
	mkdir data
test:
	pytest
