.PHONY:
	test
	wheel
	format
	clean

test:
	nosetests --with-coverage --cover-package=smartcar --cover-html --cover-html-dir=htmlcover $(args) --cover-min-percentage 97 -verbose -d

wheel:
	python setup.py bdist_wheel --universal

format:
	black ./smartcar ./tests ./setup.py $(args)

clean:
	rm -rf build dist htmlcover node_modules smartcar.egg-info
