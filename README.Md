# Istio Distributed Tracing Demo

This repo contains a simple example of a distributed tracing set up within an istio service mesh in a local k8s cluster. It's made up of 4 pods in the following architecture:
```
        OUSTIDE MESH | INSIDE MESH
request-generator - >  ingressgateway -> forward pod  ->  return pod
                     |
```

This demonstration is made up of 4 pods:
- request-generator
  - deployed outside of the mesh, used to send requests that will lead to the creation of traces
- ingressgateway
  - entrypoint into service mesh
- forward pod
  - simple app that will create an outbound request using a url that gets sent to it in an inbound request
- return pod 
  - simple app which returns the http headers that get sent to it in the request in the http response body

To use the app run the following command to exec into the request generator pod
`kubectl exec -it request-generator -- sh`

Then run the following request within the pod to send a request to the `forward` pod via the ingressgateway, which will then create another request to the `return` pod

`apk add curl`

`curl -v -X POST -H "Content-Type: application/json" -d '{"url": "http://return.tracing.svc.cluster.local/print_headers"}' -H "Host: tracing-demo.com" http://istio-ingressgateway.istio-system.svc.cluster.local/forward`


To see the traces in the tracing backend run:
`kubectl port-forward -n observability svc/jaeger-all-in-one-query 16686`

open `http://localhost:16686` in the browser

