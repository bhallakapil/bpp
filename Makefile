VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

all: venv build_bigdeal

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .

venv: $(VENV)/bin/activate

build_bigdeal:
	$(MAKE) -C bigdeal
	cp bigdeal/libbigdeal.a .
	cp bigdeal/libbigdeal.dylib .

clean:
	$(MAKE) -C bigdeal clean
	$(MAKE) -C dds clean
	rm -rf $(VENV)
	rm -f libbigdeal.a libbigdeal.dylib libdds.a libdds.dylib

.PHONY: all build_bigdeal clean venv
