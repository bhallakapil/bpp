all: build_bigdeal build_dds

build_bigdeal:
	$(MAKE) -C bigdeal
	cp bigdeal/libbigdeal.a .
	cp bigdeal/libbigdeal.dylib .

build_dds:
	$(MAKE) -C dds
	cp dds/libdds.a .
	cp dds/libdds.dylib .

clean:
	$(MAKE) -C bigdeal clean
	$(MAKE) -C dds clean
	rm -f libbigdeal.a libbigdeal.dylib libdds.a libdds.dylib

.PHONY: all build_bigdeal build_dds clean
