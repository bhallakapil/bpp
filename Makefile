VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

all: venv

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .

venv: $(VENV)/bin/activate

clean:
	$(MAKE) -C dds clean
	rm -rf $(VENV)
	rm -f libdds.a libdds.dylib redeal/*.so

.PHONY: all clean venv
