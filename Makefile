all:

.PHONY: README.md env test test3 check clean build publish install

# Run tests
test:
	@nosetests tests/
test3:
	@nosetests3 tests/
# Package
check:
	@./setup.py check
clean:
	@rm -rf build/ dist/ *.egg-info/ README.rst README.md
README.md:
	@python misc/_doc/README.py | j2 --format=json misc/_doc/README.md.j2 > README.md
README.rst: README.md
	@pandoc -f markdown -t rst -o README.rst README.md
build: README.rst
	@./setup.py build sdist bdist_wheel
publish: README.rst
	@./setup.py build sdist bdist_wheel register upload -r pypi
