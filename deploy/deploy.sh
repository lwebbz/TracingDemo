#!/bin/bash

# Create namespaces
kubectl create namespace istio-system
kubectl create namespace istio-operator
kubectl create namespace observability
kubectl create namespace tracing

# Install Istio CRDs
helm upgrade --install istio-base istio/base -n istio-system -f operator.values.yaml --wait

# Deploy istio operator
istioctl operator init --watchedNamespaces=istio-system

# Label namespaces where proxy sidecar injection should be enabled
kubectl label namespace istio-system istio-injection: enabled
kubectl label namespace tracing istio-injection: enabled

# Deploy istio controlplane and ingressgateways
kubectl apply -f controlplane-and-ingress.yaml

# Deploy gateway CR
kubectl apply -f gateway.yaml

# Deploy cert manager (needed to deploy Jaeger operator)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.6.3/cert-manager.yaml

# Deploy Jaeger tracing backend
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.53.0/jaeger-operator.yaml -n observability

# Deploy jaeger simple all-in-one CR
kubectl apply -f jaeger.yaml

# Deploy workload deployments
kubectl apply -f forward-deployment.yaml
kubectl apply -f return-deployment.yaml

# Deploy pod which we'll use to generate requests
kubectl apply -f request-generator-pod.yaml