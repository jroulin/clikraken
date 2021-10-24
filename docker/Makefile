IMAGENAME := clikraken/clikraken
DATESTR := $(shell date +%Y%m%d-%H%M%S)
CLIKRAKEN_VERSION := $(shell git rev-parse HEAD)
CLIKRAKEN_URL := $(shell git remote get-url $$(git remote))

build:
	docker build --network=host --build-arg CLIKRAKEN_VERSION=$(CLIKRAKEN_VERSION) --build-arg CLIKRAKEN_URL=$(CLIKRAKEN_URL) -t $(IMAGENAME):latest .
	docker tag $(IMAGENAME):latest $(IMAGENAME):$(DATESTR)
	docker tag $(IMAGENAME):latest $(IMAGENAME):$(CLIKRAKEN_VERSION)
	docker run --rm $(IMAGENAME):latest -V

rmi:
	docker rmi $(IMAGENAME):latest

