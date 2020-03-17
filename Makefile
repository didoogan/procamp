build:
	@docker build -t didoogan/procamp:latest .
pull:
	@docker pull didoogan/procamp:latest
cpu:
	@docker run --rm didoogan/procamp cpu
mem:
	@docker run --rm didoogan/procamp mem