.PHONY: unittest flake8 test clean

unittest:
	python3 -m unittest

flake8:
	flake8 --filename="*.py,./gspeech,./gspeech-cli"

test:
	make unittest
	make flake8

clean:
	rm -f MANIFEST
	rm -rf build dist
