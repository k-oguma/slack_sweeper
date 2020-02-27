PLUGINS := vagrant-disksize vagrant-hostsupdater vagrant-mutagen
.PHONY: all docker help
.DEFAULT_GOAL := all

help:
	@echo "Usage: make \033[36m[subCommand]\033[0m\n"
	@printf "%-35s%s\n" "make" ": Install and build for a docker environment."
	@perl -le 'printf("\033[36m%17s\033[0m\n", "[subCommand]")'
	@perl -lne ' /(.*):\s+?.*##\s+?(.*)/ and printf "%-s \033[36m%-30s\033[0m%s\n", "make", $$1, ": $$2"' $(MAKEFILE_LIST)

all: vagrant_plugin_install \
	docker

vagrant_plugin_install: ## Installing Vagrant plugins
	@vagrant plugin install $(PLUGINS)

vagrant_up: ## Starting the Vagrant
	@vagrant up

vagrant_ssh: ## SSH login to the Vagrant
	@vagrant ssh

docker: vagrant_up vagrant_ssh ## Building of the Vagrant environment

