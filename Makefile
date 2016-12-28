test:
	nosetests --with-coverage --cover-package=smartcar --cover-html --cover-html-dir=htmlcover $(args) --cover-min-percentage 98

wheel:
	python setup.py bdist_wheel --universal

clean:
	rm -r build dist htmlcover smartcar.egg-info
