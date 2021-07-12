.PHONY:
	test
	wheel
	format
	clean

test:
	pytest --cov=smartcar

wheel:
	python setup.py bdist_wheel --universal

format:
	black ./smartcar ./tests ./setup.py $(args)

clean:
	rm -rf build dist htmlcover node_modules smartcar.egg-info
