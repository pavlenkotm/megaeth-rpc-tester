.PHONY: build clean compile test run package

build:
	mvn clean compile

compile:
	mvn compile

test:
	mvn test

package:
	mvn package

run:
	mvn exec:java -Dexec.mainClass="com.web3.examples.Web3Example"

clean:
	mvn clean

install:
	mvn clean install

help:
	@echo "Available targets:"
	@echo "  build    - Clean and compile"
	@echo "  compile  - Compile only"
	@echo "  test     - Run tests"
	@echo "  package  - Create JAR"
	@echo "  run      - Run main class"
	@echo "  clean    - Clean build artifacts"
	@echo "  install  - Install to local Maven repo"
