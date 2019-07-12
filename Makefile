test:
	nosetests --with-coverage --cover-package=smartcar --cover-html --cover-html-dir=htmlcover $(args) --cover-min-percentage 97 -verbose -d

lint:
	black ./smartcar --check
	black ./tests --check

wheel:
	python setup.py bdist_wheel --universal

clean:
	rm -r build dist htmlcover smartcar.egg-info
