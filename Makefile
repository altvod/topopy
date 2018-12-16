PACKAGE_NAME = topopy


build_doc:
	rm -rf docs/apidoc
	sphinx-apidoc --no-toc --separate -o docs/apidoc ${PACKAGE_NAME}
	cd docs; make html


doc: build_doc
	xdg-open docs/_build/html/index.html


stylecheck:
	pylama topopy tests


clean:
	rm -rf .tox


test:
	PACKAGE_NAME=${PACKAGE_NAME} tox


build:
	python setup.py sdist upload
