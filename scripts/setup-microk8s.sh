#!/bin/bash

sudo snap install microk8s --classic --channel=1.30

sudo usermod -a -G microk8s $USER
mkdir -p ~/.kube
chmod 0700 ~/.kube

su - $USER
