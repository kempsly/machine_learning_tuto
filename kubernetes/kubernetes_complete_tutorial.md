# Kubernetes — Complete In-Depth Tutorial
> **The most comprehensive Kubernetes reference** — every concept, every resource, every command, and deployment on every major platform  
> Written for data scientists and ML engineers deploying production-grade systems

---

## Table of Contents

### Part 1 — Fundamentals
1. [What is Kubernetes and Why it Exists](#1-what-is-kubernetes-and-why-it-exists)
2. [How Kubernetes Works Internally](#2-how-kubernetes-works-internally)
3. [Kubernetes Architecture](#3-kubernetes-architecture)
4. [Installation — kubectl and Local Clusters](#4-installation--kubectl-and-local-clusters)
5. [Core Concepts and Terminology](#5-core-concepts-and-terminology)

### Part 2 — Core Resources
6. [Pods — The Basic Unit](#6-pods--the-basic-unit)
7. [Deployments — Managing Replicas](#7-deployments--managing-replicas)
8. [Services — Networking and Discovery](#8-services--networking-and-discovery)
9. [ConfigMaps — Configuration Management](#9-configmaps--configuration-management)
10. [Secrets — Sensitive Data](#10-secrets--sensitive-data)
11. [Namespaces — Logical Isolation](#11-namespaces--logical-isolation)
12. [ReplicaSets](#12-replicasets)
13. [StatefulSets — Stateful Applications](#13-statefulsets--stateful-applications)
14. [DaemonSets — Node-Level Services](#14-daemonsets--node-level-services)
15. [Jobs and CronJobs](#15-jobs-and-cronjobs)

### Part 3 — Storage
16. [Volumes — Container Storage](#16-volumes--container-storage)
17. [PersistentVolumes and PersistentVolumeClaims](#17-persistentvolumes-and-persistentvolumeclaims)
18. [StorageClasses — Dynamic Provisioning](#18-storageclasses--dynamic-provisioning)

### Part 4 — Networking
19. [Kubernetes Networking Model](#19-kubernetes-networking-model)
20. [Ingress — HTTP Routing](#20-ingress--http-routing)
21. [NetworkPolicies — Traffic Control](#21-networkpolicies--traffic-control)

### Part 5 — Configuration and Scaling
22. [Resource Requests and Limits](#22-resource-requests-and-limits)
23. [Horizontal Pod Autoscaler](#23-horizontal-pod-autoscaler)
24. [Vertical Pod Autoscaler](#24-vertical-pod-autoscaler)
25. [Node Affinity and Pod Scheduling](#25-node-affinity-and-pod-scheduling)
26. [Taints and Tolerations](#26-taints-and-tolerations)

### Part 6 — Observability
27. [Probes — Liveness, Readiness, Startup](#27-probes--liveness-readiness-startup)
28. [Logging in Kubernetes](#28-logging-in-kubernetes)
29. [Monitoring with Prometheus and Grafana](#29-monitoring-with-prometheus-and-grafana)

### Part 7 — Security
30. [RBAC — Role-Based Access Control](#30-rbac--role-based-access-control)
31. [ServiceAccounts](#31-serviceaccounts)
32. [Pod Security](#32-pod-security)

### Part 8 — Advanced Topics
33. [Helm — Package Manager for Kubernetes](#33-helm--package-manager-for-kubernetes)
34. [Kustomize — Configuration Management](#34-kustomize--configuration-management)
35. [Custom Resource Definitions](#35-custom-resource-definitions)

### Part 9 — ML on Kubernetes
36. [Deploying ML Models on Kubernetes](#36-deploying-ml-models-on-kubernetes)
37. [Deploying FastAPI + XGBoost on Kubernetes](#37-deploying-fastapi--xgboost-on-kubernetes)

### Part 10 — Deployment on Every Platform
38. [Local — Minikube](#38-local--minikube)
39. [Local — Kind (Kubernetes in Docker)](#39-local--kind-kubernetes-in-docker)
40. [Local — k3s (Lightweight Kubernetes)](#40-local--k3s-lightweight-kubernetes)
41. [AWS — Amazon EKS](#41-aws--amazon-eks)
42. [Google Cloud — GKE](#42-google-cloud--gke)
43. [Microsoft Azure — AKS](#43-microsoft-azure--aks)
44. [DigitalOcean — DOKS](#44-digitalocean--doks)
45. [On-Premises — kubeadm](#45-on-premises--kubeadm)

### Part 11 — Reference
46. [kubectl — Complete Command Reference](#46-kubectl--complete-command-reference)
47. [Cheat Sheet](#47-cheat-sheet)

---

# PART 1 — FUNDAMENTALS

---

## 1. What is Kubernetes and Why it Exists

### The Problem Docker Alone Cannot Solve

Docker solved the "works on my machine" problem by packaging applications into containers. But Docker alone is a single-host solution. When you have a production application serving millions of users, you face questions Docker cannot answer:

- What happens when the host machine fails? How do containers restart on another machine?
- How do you run 50 copies of your API across 10 different servers?
- How do you update your application to a new version without downtime?
- How do you automatically add more containers when traffic spikes?
- How do containers on different machines find each other?
- How do you roll back a bad deployment?

These are the problems Kubernetes was built to solve.

### What Kubernetes Is

Kubernetes (often abbreviated K8s — the 8 stands for the 8 letters between K and s) is an open-source container orchestration platform. It automates the deployment, scaling, and management of containerized applications across a cluster of machines.

Kubernetes was originally developed by Google, who had been running containerized workloads internally at massive scale for over a decade (using an internal system called Borg). Google donated Kubernetes to the Cloud Native Computing Foundation (CNCF) in 2014 and it has since become the industry standard for container orchestration.

### What Kubernetes Does

**Self-healing** — If a container crashes, Kubernetes automatically restarts it. If a node (server) fails, Kubernetes reschedules the containers that were running on it to healthy nodes.

**Horizontal scaling** — You can scale your application up or down by changing a single number. Kubernetes starts or stops containers automatically. You can even configure this to happen automatically based on CPU usage or other metrics.

**Rolling deployments** — When you update your application, Kubernetes gradually replaces old containers with new ones, ensuring some old version is always running until the new version is verified healthy. This eliminates downtime.

**Load balancing** — Kubernetes distributes traffic across all healthy running containers automatically.

**Service discovery** — Containers find each other by name through built-in DNS. You don't need to hardcode IP addresses.

**Secret and configuration management** — Kubernetes stores credentials and configuration separately from your application code and injects them securely at runtime.

**Storage orchestration** — Kubernetes automatically mounts storage from local disks, cloud providers, or network storage systems.

### The Kubernetes Mental Model

Kubernetes operates on a **declarative** model. Instead of telling Kubernetes what to do (imperative), you tell it what state you want (declarative), and Kubernetes figures out how to get there and keeps things in that state.

```yaml
# You say: "I want 3 copies of my API running at all times"
# Kubernetes makes it happen and keeps it that way

apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3    # desired state: 3 running copies
```

If one copy crashes, Kubernetes starts a new one. If a node fails, Kubernetes reschedules. You defined the desired state — Kubernetes maintains it perpetually.

---

## 2. How Kubernetes Works Internally

### The Control Loop

Kubernetes is built around a fundamental pattern called the **control loop** (or reconciliation loop). Every component in Kubernetes follows this pattern:

1. Observe the current state of the cluster
2. Compare it to the desired state (what you declared in YAML)
3. Take actions to make current state match desired state
4. Repeat forever

```
┌────────────────────────────────────┐
│         Control Loop               │
│                                    │
│  Current State → Compare → Desired │
│       ↑                     State  │
│       │                      │     │
│       └──── Take Action ─────┘     │
└────────────────────────────────────┘
```

For example, if you declare "I want 3 replicas" and one pod crashes, the ReplicaSet controller observes current state is 2, desired is 3, so it creates a new pod.

### The etcd Database

All cluster state is stored in **etcd**, a distributed key-value store. etcd is the single source of truth for Kubernetes. Everything you create — deployments, services, pods, secrets — is stored here.

etcd uses the Raft consensus algorithm to ensure data consistency across multiple copies. Losing etcd means losing your entire cluster state.

### How a Pod Gets Scheduled

When you create a Pod, here is exactly what happens:

1. You run `kubectl apply -f pod.yaml`
2. kubectl sends an API request to the API Server
3. The API Server validates the request and stores the pod spec in etcd (marked as "Pending")
4. The Scheduler watches for unscheduled pods, selects the best node based on resource availability and constraints, and writes the node assignment to etcd
5. The Kubelet on the selected node watches etcd for pods assigned to it, calls the container runtime to pull the image and start the container
6. The Kubelet reports the pod status back to the API Server, which writes it to etcd
7. The pod is now "Running"

---

## 3. Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CONTROL PLANE                           │
│                                                                 │
│  ┌──────────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐  │
│  │  API Server  │  │ Scheduler │  │Controller │  │  etcd   │  │
│  │(kube-apiserver)│ │           │  │  Manager  │  │         │  │
│  └──────────────┘  └───────────┘  └───────────┘  └─────────┘  │
└─────────────────────────────────────────────────────────────────┘
            │                  │                  │
     ┌──────┘          ┌───────┘          ┌───────┘
     ▼                 ▼                  ▼
┌──────────┐     ┌──────────┐     ┌──────────┐
│  NODE 1  │     │  NODE 2  │     │  NODE 3  │
│          │     │          │     │          │
│ kubelet  │     │ kubelet  │     │ kubelet  │
│ kube-proxy│    │ kube-proxy│    │ kube-proxy│
│ container│     │ container│     │ container│
│ runtime  │     │ runtime  │     │ runtime  │
│          │     │          │     │          │
│ [Pod]    │     │ [Pod]    │     │ [Pod]    │
│ [Pod]    │     │ [Pod]    │     │ [Pod]    │
└──────────┘     └──────────┘     └──────────┘
```

### Control Plane Components

**kube-apiserver** — The front door of Kubernetes. All communication (kubectl, internal components, external tools) goes through the API server. It validates requests, authenticates/authorizes them, and updates etcd. It is stateless and can be scaled horizontally.

**etcd** — The cluster's database. Stores all cluster state as key-value pairs. Must be backed up regularly. In production, run as a 3 or 5-node cluster for high availability.

**kube-scheduler** — Watches for newly created pods with no assigned node. Selects the best node based on: resource requirements, node selectors, affinity/anti-affinity rules, taints and tolerations, and available resources. Does NOT start the pod — just assigns it to a node.

**kube-controller-manager** — Runs multiple controllers as a single process:
- **ReplicaSet Controller** — ensures the desired number of pod replicas are running
- **Deployment Controller** — manages rolling updates
- **Node Controller** — monitors node health, marks nodes as unavailable
- **Endpoints Controller** — maintains the list of pods behind a Service
- **Service Account Controller** — creates default service accounts for namespaces

**cloud-controller-manager** — Integrates with cloud provider APIs (AWS, GCP, Azure) to manage cloud resources like load balancers and storage volumes.

### Node Components

**kubelet** — An agent that runs on every node. Watches the API server for pods assigned to its node. Instructs the container runtime to pull images and start containers. Reports pod status back to the API server. Runs liveness/readiness probes.

**kube-proxy** — Maintains network rules on each node. Implements Kubernetes Services by managing iptables or IPVS rules that forward traffic to the correct pods.

**Container Runtime** — The software that actually runs containers. Kubernetes supports any OCI-compliant runtime: containerd (most common), CRI-O, Docker (deprecated as runtime).

---

## 4. Installation — kubectl and Local Clusters

### Install kubectl

```bash
# ── Mac ───────────────────────────────────────────────────────
brew install kubectl

# or with curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# ── Linux ─────────────────────────────────────────────────────
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# ── Windows ───────────────────────────────────────────────────
# Download from https://dl.k8s.io/release/stable.txt/bin/windows/amd64/kubectl.exe
# Or with winget:
winget install Kubernetes.kubectl

# verify
kubectl version --client
kubectl version --short    # shorter output

# enable autocompletion (bash)
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc

# enable autocompletion (zsh)
source <(kubectl completion zsh)
echo "source <(kubectl completion zsh)" >> ~/.zshrc

# useful alias
alias k=kubectl
complete -F __start_kubectl k    # autocompletion for alias
```

### Configure kubectl

```bash
# kubectl uses a config file at ~/.kube/config (kubeconfig)
# contains: clusters, users, and contexts

# view current config
kubectl config view

# list contexts (each context = cluster + user + namespace)
kubectl config get-contexts

# switch context
kubectl config use-context my-cluster

# set default namespace for current context
kubectl config set-context --current --namespace=my-namespace

# add a new cluster to kubeconfig
kubectl config set-cluster my-cluster \
    --server=https://my-cluster.example.com \
    --certificate-authority=ca.crt

# merge multiple kubeconfigs
KUBECONFIG=~/.kube/config:~/.kube/another-config kubectl config view --merge --flatten > ~/.kube/merged-config
```

---

## 5. Core Concepts and Terminology

### The Object Model

Everything in Kubernetes is an **object**. Objects are persistent entities that represent the desired state of your cluster. Every object has:

- **apiVersion** — which API version to use
- **kind** — what type of object (Pod, Deployment, Service, etc.)
- **metadata** — name, namespace, labels, annotations
- **spec** — desired state (what you want)
- **status** — current state (what actually is) — written by Kubernetes, not you

```yaml
apiVersion: apps/v1        # API group/version
kind: Deployment           # object type
metadata:
  name: my-app             # unique name within namespace
  namespace: production    # which namespace
  labels:                  # key-value pairs for organization
    app: my-app
    version: "1.0"
  annotations:             # non-identifying metadata
    description: "Main application deployment"
spec:                      # desired state — YOU write this
  replicas: 3
status:                    # current state — Kubernetes writes this
  availableReplicas: 3
```

### Labels and Selectors

Labels are key-value pairs attached to objects. They are the primary mechanism Kubernetes uses to connect objects to each other.

```yaml
# label a pod
metadata:
  labels:
    app: nginx
    environment: production
    version: "1.5"
    tier: frontend

# select pods with a label selector
selector:
  matchLabels:
    app: nginx
    environment: production
```

Selectors are how Services find their Pods, how Deployments manage their ReplicaSets, and how you filter resources in kubectl.

### Annotations

Annotations are also key-value pairs but for non-identifying metadata. They are not used for selection but for attaching arbitrary metadata.

```yaml
metadata:
  annotations:
    deployment.kubernetes.io/revision: "3"
    kubernetes.io/change-cause: "Updated to v2.0"
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
```

### Namespaces

Namespaces provide logical isolation within a cluster. Resources in different namespaces are isolated from each other (in terms of naming and access control) but share the same physical cluster.

```bash
# default namespaces
kubectl get namespaces
# NAME              STATUS
# default           Active    ← your resources go here unless specified
# kube-system       Active    ← Kubernetes system components
# kube-public       Active    ← publicly readable resources
# kube-node-lease   Active    ← node heartbeat leases
```

---

# PART 2 — CORE RESOURCES

---

## 6. Pods — The Basic Unit

A Pod is the smallest deployable unit in Kubernetes. A Pod contains one or more containers that share:
- The same network namespace (same IP address and port space)
- The same storage volumes
- The same lifecycle

In practice, most Pods contain a single container. Multi-container Pods are used for sidecar patterns (e.g., a logging agent alongside the main application).

```yaml
# pod.yaml — single container Pod
apiVersion: v1
kind: Pod
metadata:
  name: finsaight-api
  namespace: default
  labels:
    app: finsaight
    tier: api
spec:
  containers:
    - name: api                              # container name
      image: kempsly/finsaight-api:1.0      # image to use
      imagePullPolicy: Always               # Always | IfNotPresent | Never

      # ports to expose (informational)
      ports:
        - containerPort: 8000
          protocol: TCP

      # environment variables
      env:
        - name: PORT
          value: "8000"
        - name: DEBUG
          value: "false"
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: groq-api-key

      # resource requests and limits
      resources:
        requests:                 # minimum guaranteed resources
          memory: "256Mi"
          cpu: "250m"            # 250 millicores = 0.25 CPU
        limits:                  # maximum allowed resources
          memory: "1Gi"
          cpu: "1000m"           # 1 full CPU

      # liveness probe — restart if fails
      livenessProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 15
        periodSeconds: 30
        timeoutSeconds: 10
        failureThreshold: 3

      # readiness probe — remove from service if fails
      readinessProbe:
        httpGet:
          path: /ready
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 10

      # volume mounts
      volumeMounts:
        - name: model-storage
          mountPath: /app/models

  # volumes available to containers in this Pod
  volumes:
    - name: model-storage
      persistentVolumeClaim:
        claimName: ml-models-pvc

  # restart policy
  restartPolicy: Always        # Always | OnFailure | Never

  # service account
  serviceAccountName: default

  # image pull secrets (for private registries)
  imagePullSecrets:
    - name: registry-credentials
```

```bash
# create pod
kubectl apply -f pod.yaml

# get pods
kubectl get pods
kubectl get pods -o wide           # show node, IP
kubectl get pods -n kube-system    # in specific namespace
kubectl get pods --all-namespaces  # all namespaces
kubectl get pods -w                # watch for changes

# describe pod (human-readable details + events)
kubectl describe pod finsaight-api

# pod logs
kubectl logs finsaight-api
kubectl logs -f finsaight-api              # follow
kubectl logs --tail=100 finsaight-api      # last 100 lines
kubectl logs finsaight-api -c api          # specific container (multi-container pod)
kubectl logs --previous finsaight-api      # logs from previous (crashed) container

# exec into pod
kubectl exec -it finsaight-api -- bash
kubectl exec -it finsaight-api -- sh       # if bash not available
kubectl exec finsaight-api -- ls /app

# copy files
kubectl cp finsaight-api:/app/logs/app.log ./app.log
kubectl cp ./model.pkl finsaight-api:/app/models/

# delete pod
kubectl delete pod finsaight-api
kubectl delete -f pod.yaml

# get pod YAML (see full spec including status)
kubectl get pod finsaight-api -o yaml
kubectl get pod finsaight-api -o json
```

### Multi-Container Pod Patterns

```yaml
# sidecar pattern — log shipper alongside main app
spec:
  containers:
    - name: api                       # main container
      image: kempsly/finsaight-api:1.0
      volumeMounts:
        - name: logs
          mountPath: /app/logs

    - name: log-shipper               # sidecar container
      image: fluent/fluentd:v1.16
      volumeMounts:
        - name: logs
          mountPath: /logs            # reads main container's logs
          readOnly: true

  volumes:
    - name: logs
      emptyDir: {}    # shared volume between containers
```

---

## 7. Deployments — Managing Replicas

A Deployment manages a set of identical Pods. It ensures the desired number of replicas are running and handles rolling updates and rollbacks.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: finsaight-api
  namespace: production
  labels:
    app: finsaight
  annotations:
    kubernetes.io/change-cause: "Update to v2.0 — add hybrid search"
spec:
  # number of pod replicas to run
  replicas: 3

  # which pods this deployment manages (must match pod template labels)
  selector:
    matchLabels:
      app: finsaight
      tier: api

  # rolling update strategy
  strategy:
    type: RollingUpdate           # RollingUpdate | Recreate
    rollingUpdate:
      maxUnavailable: 1           # max pods that can be unavailable during update
      maxSurge: 1                 # max extra pods during update (above replicas)
      # with replicas=3, maxUnavailable=1, maxSurge=1:
      # during update: min 2 pods running, max 4 pods total

  # how many old ReplicaSets to keep (for rollback)
  revisionHistoryLimit: 10

  # min seconds a pod must be ready before considered available
  minReadySeconds: 5

  # pod template — used to create pods
  template:
    metadata:
      labels:
        app: finsaight
        tier: api                 # must match selector above
    spec:
      containers:
        - name: api
          image: kempsly/finsaight-api:2.0
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "1Gi"
              cpu: "1000m"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
```

```bash
# create deployment
kubectl apply -f deployment.yaml

# get deployments
kubectl get deployments
kubectl get deploy                 # short form
kubectl get deploy -o wide         # show images and selectors

# describe deployment
kubectl describe deployment finsaight-api

# scale deployment
kubectl scale deployment finsaight-api --replicas=5
kubectl scale deploy finsaight-api --replicas=1   # scale down

# update image (triggers rolling update)
kubectl set image deployment/finsaight-api api=kempsly/finsaight-api:3.0

# watch rolling update
kubectl rollout status deployment/finsaight-api
kubectl get pods -w    # watch pods being replaced

# rollout history
kubectl rollout history deployment/finsaight-api
kubectl rollout history deployment/finsaight-api --revision=2

# rollback to previous version
kubectl rollout undo deployment/finsaight-api
kubectl rollout undo deployment/finsaight-api --to-revision=2

# pause rolling update
kubectl rollout pause deployment/finsaight-api

# resume rolling update
kubectl rollout resume deployment/finsaight-api

# restart all pods (force recreate without changing spec)
kubectl rollout restart deployment/finsaight-api

# delete deployment
kubectl delete deployment finsaight-api
```

### Recreate Strategy

```yaml
strategy:
  type: Recreate
  # kills ALL old pods before creating new ones
  # causes downtime — use only when you cannot run two versions simultaneously
  # common for: database schema changes, GPU workloads (only one can use GPU)
```

---

## 8. Services — Networking and Discovery

Pods are ephemeral — they get new IP addresses every time they restart. A Service provides a stable IP address and DNS name that automatically routes to healthy Pods.

### Service Types

**ClusterIP** (default) — exposes the service on a cluster-internal IP. Only reachable within the cluster.

**NodePort** — exposes the service on each node's IP at a static port (30000–32767). Reachable from outside the cluster.

**LoadBalancer** — provisions an external load balancer from the cloud provider. The standard way to expose services on cloud platforms.

**ExternalName** — maps the service to an external DNS name.

```yaml
# clusterip-service.yaml — internal service
apiVersion: v1
kind: Service
metadata:
  name: finsaight-api-svc
  namespace: production
spec:
  type: ClusterIP             # default type
  selector:
    app: finsaight
    tier: api                 # routes to pods with these labels
  ports:
    - name: http
      protocol: TCP
      port: 80                # service port (what clients connect to)
      targetPort: 8000        # container port (what pod listens on)
    - name: metrics
      protocol: TCP
      port: 9090
      targetPort: 9090
```

```yaml
# nodeport-service.yaml — expose to outside (for development)
apiVersion: v1
kind: Service
metadata:
  name: finsaight-api-nodeport
spec:
  type: NodePort
  selector:
    app: finsaight
  ports:
    - port: 80
      targetPort: 8000
      nodePort: 30080    # must be 30000-32767, or omit for auto-assignment
```

```yaml
# loadbalancer-service.yaml — cloud load balancer (production)
apiVersion: v1
kind: Service
metadata:
  name: finsaight-api-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"    # AWS NLB
spec:
  type: LoadBalancer
  selector:
    app: finsaight
  ports:
    - port: 80
      targetPort: 8000
```

```yaml
# headless service — no cluster IP, DNS returns pod IPs directly
# used with StatefulSets for stable pod DNS names
apiVersion: v1
kind: Service
metadata:
  name: finsaight-headless
spec:
  clusterIP: None           # headless
  selector:
    app: finsaight
  ports:
    - port: 8000
```

```bash
# get services
kubectl get services
kubectl get svc            # short form
kubectl get svc -o wide    # show selector and cluster IP

# describe service
kubectl describe svc finsaight-api-svc

# expose a deployment as a service (quick way)
kubectl expose deployment finsaight-api --port=80 --target-port=8000

# get endpoints (actual pod IPs behind a service)
kubectl get endpoints finsaight-api-svc

# port-forward for local testing (no service needed)
kubectl port-forward pod/finsaight-api-xxx 8080:8000
kubectl port-forward deployment/finsaight-api 8080:8000
kubectl port-forward svc/finsaight-api-svc 8080:80
# now: curl http://localhost:8080
```

### DNS in Kubernetes

Every Service gets a DNS name automatically:
```
<service-name>.<namespace>.svc.cluster.local

# examples:
finsaight-api-svc.production.svc.cluster.local
db.production.svc.cluster.local

# within the same namespace, just use the service name:
http://finsaight-api-svc/endpoint
postgresql://db:5432/mydb
```

---

## 9. ConfigMaps — Configuration Management

ConfigMaps store non-sensitive configuration data as key-value pairs.

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: finsaight-config
  namespace: production
data:
  # key-value pairs
  APP_ENV: "production"
  LOG_LEVEL: "info"
  PORT: "8000"
  MAX_WORKERS: "4"

  # multi-line config file
  app.properties: |
    server.port=8000
    log.level=info
    feature.hybrid_search=true

  # JSON config
  config.json: |
    {
      "model": "llama-3.3-70b-versatile",
      "max_tokens": 2048,
      "temperature": 0.1
    }
```

```yaml
# using configmap in a pod
spec:
  containers:
    - name: api
      image: kempsly/finsaight-api:1.0

      # inject all configmap keys as environment variables
      envFrom:
        - configMapRef:
            name: finsaight-config

      # inject specific keys
      env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: finsaight-config
              key: APP_ENV

      # mount configmap as files
      volumeMounts:
        - name: config-volume
          mountPath: /app/config

  volumes:
    - name: config-volume
      configMap:
        name: finsaight-config
        items:
          - key: config.json
            path: config.json       # mounted at /app/config/config.json
          - key: app.properties
            path: app.properties    # mounted at /app/config/app.properties
```

```bash
# create configmap from literal values
kubectl create configmap finsaight-config \
    --from-literal=APP_ENV=production \
    --from-literal=PORT=8000

# create from file
kubectl create configmap app-config --from-file=config.json
kubectl create configmap app-config --from-file=./config/   # entire directory

# get configmaps
kubectl get configmaps
kubectl get cm               # short form
kubectl describe cm finsaight-config
kubectl get cm finsaight-config -o yaml

# edit configmap
kubectl edit cm finsaight-config

# delete
kubectl delete cm finsaight-config
```

---

## 10. Secrets — Sensitive Data

Secrets are like ConfigMaps but for sensitive data. Values are base64-encoded (NOT encrypted by default — enable encryption at rest for production).

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
  namespace: production
type: Opaque             # generic secret
data:
  # values must be base64-encoded
  # echo -n "my_secret_key" | base64
  groq-api-key: bXlfc2VjcmV0X2tleQ==
  db-password: cGFzc3dvcmQxMjM=
  jwt-secret: c3VwZXJzZWNyZXRqd3Rz

stringData:              # plain text (Kubernetes encodes automatically)
  api-url: "https://api.groq.com"
```

```yaml
# docker registry secret (for private images)
apiVersion: v1
kind: Secret
metadata:
  name: registry-credentials
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
```

```yaml
# using secrets in a pod
spec:
  containers:
    - name: api
      # inject all secret keys as environment variables
      envFrom:
        - secretRef:
            name: api-secrets

      # inject specific secret key
      env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: groq-api-key

      # mount secret as files (more secure — not in env)
      volumeMounts:
        - name: secrets-volume
          mountPath: /app/secrets
          readOnly: true

  volumes:
    - name: secrets-volume
      secret:
        secretName: api-secrets
        defaultMode: 0400    # read-only by owner only
```

```bash
# create secret from literal (never write secret values in YAML)
kubectl create secret generic api-secrets \
    --from-literal=groq-api-key=sk-abc123 \
    --from-literal=db-password=mysecretpassword

# create from file
kubectl create secret generic tls-certs \
    --from-file=tls.crt --from-file=tls.key

# create TLS secret
kubectl create secret tls my-tls-secret \
    --cert=tls.crt --key=tls.key

# create docker registry secret
kubectl create secret docker-registry registry-credentials \
    --docker-server=registry.company.com \
    --docker-username=myuser \
    --docker-password=mypassword \
    --docker-email=my@email.com

# get secrets (values are hidden)
kubectl get secrets
kubectl describe secret api-secrets

# view decoded secret value
kubectl get secret api-secrets -o jsonpath='{.data.groq-api-key}' | base64 --decode

# delete
kubectl delete secret api-secrets
```

---

## 11. Namespaces — Logical Isolation

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: finsaight
```

```bash
# create namespace
kubectl create namespace production
kubectl apply -f namespace.yaml

# list namespaces
kubectl get namespaces
kubectl get ns              # short form

# run commands in a namespace
kubectl get pods -n production
kubectl get all -n production    # all resources

# set default namespace (so you don't have to type -n every time)
kubectl config set-context --current --namespace=production

# delete namespace (deletes ALL resources inside)
kubectl delete namespace production
```

### Resource Quotas per Namespace

```yaml
# resource-quota.yaml — limit total resources in a namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"          # total CPU requests
    requests.memory: 20Gi       # total memory requests
    limits.cpu: "20"            # total CPU limits
    limits.memory: 40Gi         # total memory limits
    pods: "50"                  # max number of pods
    services: "20"              # max number of services
    persistentvolumeclaims: "10"
    secrets: "30"
    configmaps: "30"
```

```yaml
# limitrange.yaml — default and max limits per container
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:                  # default limit if not specified
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:           # default request if not specified
        cpu: "100m"
        memory: "128Mi"
      max:                      # maximum allowed
        cpu: "4"
        memory: "8Gi"
      min:                      # minimum allowed
        cpu: "50m"
        memory: "64Mi"
```

---

## 12. ReplicaSets

A ReplicaSet ensures a specified number of pod replicas are running at any time. In practice, you almost never create ReplicaSets directly — Deployments create and manage them for you.

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: finsaight-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: finsaight
  template:
    metadata:
      labels:
        app: finsaight
    spec:
      containers:
        - name: api
          image: kempsly/finsaight-api:1.0
```

---

## 13. StatefulSets — Stateful Applications

StatefulSets are like Deployments but for applications that need stable, persistent identities. Use them for databases, message queues, distributed caches — anything that needs:
- Stable, unique network identifiers
- Stable persistent storage
- Ordered, graceful deployment and scaling

```yaml
# statefulset.yaml — PostgreSQL example
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: production
spec:
  serviceName: postgres-headless    # must match a headless service name
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:15.2
          env:
            - name: POSTGRES_USER
              value: user
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
            - name: POSTGRES_DB
              value: finsaight
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data

  # volumeClaimTemplates creates a unique PVC for each pod
  # postgres-0 gets postgres-data-postgres-0
  # postgres-1 gets postgres-data-postgres-1
  volumeClaimTemplates:
    - metadata:
        name: postgres-data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: "standard"
        resources:
          requests:
            storage: 20Gi
```

```yaml
# headless service required by StatefulSet
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
    - port: 5432
```

StatefulSet pods have stable DNS names:
```
postgres-0.postgres-headless.production.svc.cluster.local
postgres-1.postgres-headless.production.svc.cluster.local
postgres-2.postgres-headless.production.svc.cluster.local
```

---

## 14. DaemonSets — Node-Level Services

A DaemonSet ensures one copy of a pod runs on every node (or selected nodes). Used for node-level agents: log collectors, monitoring agents, network plugins.

```yaml
# daemonset.yaml — log collector on every node
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          effect: NoSchedule                        # run on control plane nodes too
      containers:
        - name: fluentd
          image: fluent/fluentd-kubernetes-daemonset:v1.16
          env:
            - name: FLUENT_ELASTICSEARCH_HOST
              value: elasticsearch.logging
          volumeMounts:
            - name: varlog
              mountPath: /var/log               # access node logs
            - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
```

---

## 15. Jobs and CronJobs

### Jobs — Run-to-Completion Tasks

```yaml
# job.yaml — ML model training job
apiVersion: batch/v1
kind: Job
metadata:
  name: train-model
  namespace: production
spec:
  completions: 1          # run until 1 successful completion
  parallelism: 1          # run 1 pod at a time
  backoffLimit: 3         # retry up to 3 times on failure
  activeDeadlineSeconds: 3600   # kill job if running more than 1 hour
  ttlSecondsAfterFinished: 3600 # clean up 1 hour after completion

  template:
    spec:
      restartPolicy: OnFailure   # Never | OnFailure (required for Jobs)
      containers:
        - name: trainer
          image: kempsly/ml-trainer:1.0
          command: ["python", "train.py"]
          args: ["--model", "xgboost", "--dataset", "credit_default"]
          resources:
            requests:
              memory: "4Gi"
              cpu: "2000m"
            limits:
              memory: "8Gi"
              cpu: "4000m"
          volumeMounts:
            - name: model-storage
              mountPath: /app/models
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: ml-models-pvc
```

### CronJobs — Scheduled Tasks

```yaml
# cronjob.yaml — scheduled report generation
apiVersion: batch/v1
kind: CronJob
metadata:
  name: generate-report
  namespace: production
spec:
  schedule: "0 6 * * *"          # every day at 6am (cron syntax)
  # ┌─── minute (0-59)
  # │ ┌─── hour (0-23)
  # │ │ ┌─── day of month (1-31)
  # │ │ │ ┌─── month (1-12)
  # │ │ │ │ ┌─── day of week (0-7)
  # 0 6 * * *  = every day at 6am

  timeZone: "Europe/Paris"
  concurrencyPolicy: Forbid       # Allow | Forbid | Replace
  successfulJobsHistoryLimit: 3   # keep last 3 successful jobs
  failedJobsHistoryLimit: 1       # keep last 1 failed job
  startingDeadlineSeconds: 300    # fail if can't start within 5 minutes

  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: reporter
              image: kempsly/report-generator:1.0
              command: ["python", "generate_report.py"]
              env:
                - name: REPORT_DATE
                  value: "yesterday"
```

```bash
# manually trigger a cronjob
kubectl create job --from=cronjob/generate-report manual-report-$(date +%s)

# get jobs
kubectl get jobs
kubectl get cronjobs

# watch job completion
kubectl get jobs -w
```

---

# PART 3 — STORAGE

---

## 16. Volumes — Container Storage

Unlike Docker volumes, Kubernetes volumes have the same lifetime as the Pod they belong to. When the Pod is deleted, the volume is deleted (unless using PersistentVolumes).

```yaml
spec:
  volumes:
    # emptyDir — created fresh when Pod starts, deleted when Pod ends
    # used for: temporary scratch space, sharing files between containers
    - name: cache
      emptyDir: {}
    - name: cache-memory
      emptyDir:
        medium: Memory          # stored in RAM (tmpfs) — faster but uses memory
        sizeLimit: 1Gi

    # hostPath — mounts a file or directory from the host node
    # use with caution — couples pod to specific node
    - name: host-logs
      hostPath:
        path: /var/log
        type: Directory         # Directory | File | DirectoryOrCreate | FileOrCreate

    # configMap and secret volumes (covered in sections 9-10)
    - name: config-files
      configMap:
        name: app-config

    # projected volume — combine multiple sources
    - name: combined
      projected:
        sources:
          - configMap:
              name: app-config
          - secret:
              name: app-secrets
          - serviceAccountToken:
              path: token
              expirationSeconds: 3600

    # PVC — persistent storage (covered in section 17)
    - name: ml-models
      persistentVolumeClaim:
        claimName: ml-models-pvc
```

---

## 17. PersistentVolumes and PersistentVolumeClaims

PersistentVolumes (PV) and PersistentVolumeClaims (PVC) decouple storage provisioning from storage consumption.

- **PersistentVolume (PV)** — a piece of storage provisioned by an administrator or dynamically by a StorageClass. It has its own lifecycle independent of pods.
- **PersistentVolumeClaim (PVC)** — a request for storage by a user. It specifies size and access mode. Kubernetes binds it to a matching PV.

```yaml
# persistentvolume.yaml — admin creates this
apiVersion: v1
kind: PersistentVolume
metadata:
  name: ml-models-pv
spec:
  capacity:
    storage: 50Gi
  accessModes:
    - ReadWriteOnce             # RWO: one node read-write
    # - ReadOnlyMany            # ROX: many nodes read-only
    # - ReadWriteMany           # RWX: many nodes read-write
    # - ReadWriteOncePod        # RWOP: one pod read-write (K8s 1.22+)
  persistentVolumeReclaimPolicy: Retain    # Retain | Recycle | Delete
  storageClassName: standard
  hostPath:                     # for local development
    path: /data/ml-models
  # for AWS EBS:
  # awsElasticBlockStore:
  #   volumeID: vol-0abc123def456
  #   fsType: ext4
  # for NFS:
  # nfs:
  #   server: 192.168.1.100
  #   path: /exports/ml-models
```

```yaml
# persistentvolumeclaim.yaml — developer creates this
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ml-models-pvc
  namespace: production
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard     # match the PV's storageClassName
  resources:
    requests:
      storage: 20Gi              # request 20GB (must be <= PV capacity)
```

```bash
# get PVs and PVCs
kubectl get pv
kubectl get pvc
kubectl get pvc -n production

# describe
kubectl describe pvc ml-models-pvc

# PVC status
# Bound   = successfully bound to a PV
# Pending = no matching PV found
# Lost    = bound PV was deleted
```

---

## 18. StorageClasses — Dynamic Provisioning

StorageClasses enable dynamic provisioning — PVs are created automatically when a PVC is created, without needing an admin to pre-create them.

```yaml
# storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"    # set as default
provisioner: kubernetes.io/aws-ebs                         # AWS EBS provisioner
parameters:
  type: gp3                       # gp2 | gp3 | io1 | io2
  iopsPerGB: "10"
  fsType: ext4
  encrypted: "true"
reclaimPolicy: Delete             # Delete | Retain
allowVolumeExpansion: true        # allow resizing PVCs
volumeBindingMode: WaitForFirstConsumer   # Immediate | WaitForFirstConsumer
```

```yaml
# PVC using StorageClass (dynamic provisioning)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ml-models-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd    # references the StorageClass
  resources:
    requests:
      storage: 50Gi
  # Kubernetes automatically creates a 50Gi gp3 EBS volume
```

---

# PART 4 — NETWORKING

---

## 19. Kubernetes Networking Model

Kubernetes has four networking requirements:
1. Every pod gets its own IP address
2. Pods on any node can communicate with all pods on any other node without NAT
3. Agents on a node can communicate with all pods on that node
4. Each pod sees its own IP the same way others see it

This model is implemented by **Container Network Interface (CNI) plugins**:
- **Calico** — most popular, supports NetworkPolicies
- **Flannel** — simple, no NetworkPolicies
- **Cilium** — eBPF-based, high performance, observability
- **Weave** — easy setup

---

## 20. Ingress — HTTP Routing

An Ingress exposes HTTP/HTTPS routes to Services within the cluster. It provides:
- Path-based routing
- Host-based routing
- TLS termination
- Load balancing

You need an **Ingress Controller** for Ingress to work (nginx-ingress, Traefik, AWS ALB, GCP Cloud Load Balancing).

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: finsaight-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/use-regex: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"    # auto TLS
spec:
  ingressClassName: nginx

  # TLS configuration
  tls:
    - hosts:
        - api.finsaight.natixis.com
      secretName: finsaight-tls

  rules:
    # host-based routing
    - host: api.finsaight.natixis.com
      http:
        paths:
          # path-based routing
          - path: /api/v1
            pathType: Prefix
            backend:
              service:
                name: finsaight-api-svc
                port:
                  number: 80
          - path: /mlflow
            pathType: Prefix
            backend:
              service:
                name: mlflow-svc
                port:
                  number: 5000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-svc
                port:
                  number: 80
```

```bash
# install nginx ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# get ingress
kubectl get ingress -n production
kubectl describe ingress finsaight-ingress -n production

# get ingress controller external IP
kubectl get svc -n ingress-nginx
```

---

## 21. NetworkPolicies — Traffic Control

By default, all pods can communicate with all other pods. NetworkPolicies restrict this.

```yaml
# networkpolicy.yaml — allow only specific traffic to the api
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: finsaight
      tier: api                  # apply to api pods

  policyTypes:
    - Ingress
    - Egress

  ingress:
    # allow traffic from nginx ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8000

    # allow traffic from within production namespace
    - from:
        - podSelector:
            matchLabels:
              environment: production
      ports:
        - protocol: TCP
          port: 8000

  egress:
    # allow traffic to database
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432

    # allow DNS
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53
```

---

# PART 5 — CONFIGURATION AND SCALING

---

## 22. Resource Requests and Limits

```yaml
spec:
  containers:
    - name: api
      resources:
        requests:
          # REQUESTS: minimum guaranteed resources
          # Scheduler uses this to find a suitable node
          # Node must have at least this much available
          memory: "256Mi"   # 256 mebibytes
          cpu: "250m"       # 250 millicores = 0.25 of one CPU core

        limits:
          # LIMITS: maximum allowed resources
          # Container is killed (OOMKilled) if it exceeds memory limit
          # Container is throttled if it exceeds CPU limit
          memory: "1Gi"     # 1 gibibyte
          cpu: "1000m"      # 1000 millicores = 1 full CPU

# CPU units:
# 1 CPU = 1000m
# 0.5 CPU = 500m
# 0.1 CPU = 100m
# Can use decimal: 0.5 = 500m

# Memory units:
# Ki = kibibyte (1024 bytes)
# Mi = mebibyte (1024 Ki)
# Gi = gibibyte (1024 Mi)
# K, M, G = decimal (1000, 1000K, 1000M)
```

### QoS Classes

Kubernetes assigns a QoS class based on resource configuration:

**Guaranteed** — requests == limits for all containers. Highest priority, never OOM killed unless exceeding limits.

**Burstable** — requests < limits. Medium priority.

**BestEffort** — no requests or limits. Lowest priority, first to be killed when node is under pressure.

---

## 23. Horizontal Pod Autoscaler

HPA automatically scales the number of pod replicas based on observed metrics.

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: finsaight-api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: finsaight-api

  minReplicas: 2      # never scale below 2
  maxReplicas: 20     # never scale above 20

  metrics:
    # CPU-based scaling
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70    # target 70% CPU utilization

    # Memory-based scaling
    - type: Resource
      resource:
        name: memory
        target:
          type: AverageValue
          averageValue: 512Mi

    # Custom metric (e.g., requests per second)
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"

  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300    # wait 5 min before scaling down
      policies:
        - type: Percent
          value: 25                       # scale down max 25% per minute
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0      # scale up immediately
      policies:
        - type: Percent
          value: 100                      # can double replicas per minute
          periodSeconds: 60
```

```bash
# install metrics server (required for HPA)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# create HPA from command line
kubectl autoscale deployment finsaight-api --cpu-percent=70 --min=2 --max=20

# get HPA status
kubectl get hpa
kubectl describe hpa finsaight-api-hpa

# watch HPA
kubectl get hpa -w
```

---

## 24. Vertical Pod Autoscaler

VPA automatically adjusts CPU and memory requests/limits based on actual usage.

```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: finsaight-api-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: finsaight-api
  updatePolicy:
    updateMode: "Auto"    # Auto | Recreate | Initial | Off
    # Auto: evicts and recreates pods with updated resources
    # Off: only provides recommendations without applying them
  resourcePolicy:
    containerPolicies:
      - containerName: api
        minAllowed:
          cpu: "100m"
          memory: "128Mi"
        maxAllowed:
          cpu: "4"
          memory: "8Gi"
```

---

## 25. Node Affinity and Pod Scheduling

Control which nodes your pods can be scheduled on.

```yaml
spec:
  affinity:
    # nodeAffinity — constrain which nodes pod can run on
    nodeAffinity:
      # REQUIRED — pod won't schedule if no matching node
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: kubernetes.io/arch
                operator: In
                values:
                  - amd64
              - key: node.kubernetes.io/instance-type
                operator: In
                values:
                  - m5.xlarge
                  - m5.2xlarge

      # PREFERRED — scheduler tries to place here but not required
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          preference:
            matchExpressions:
              - key: availability-zone
                operator: In
                values:
                  - eu-west-1a

    # podAntiAffinity — spread pods across nodes (high availability)
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchExpressions:
              - key: app
                operator: In
                values:
                  - finsaight
          topologyKey: kubernetes.io/hostname
          # this ensures no two finsaight pods run on the same node
```

---

## 26. Taints and Tolerations

Taints prevent pods from being scheduled on a node. Tolerations allow specific pods to override taints.

```bash
# add a taint to a node
kubectl taint nodes node1 gpu=true:NoSchedule
# key=value:effect
# effects: NoSchedule | PreferNoSchedule | NoExecute

# remove a taint
kubectl taint nodes node1 gpu=true:NoSchedule-
```

```yaml
# only pods with this toleration can run on tainted nodes
spec:
  tolerations:
    - key: "gpu"
      operator: "Equal"
      value: "true"
      effect: "NoSchedule"
```

---

# PART 6 — OBSERVABILITY

---

## 27. Probes — Liveness, Readiness, Startup

```yaml
spec:
  containers:
    - name: api

      # STARTUP PROBE — allow slow startup without failing liveness
      # only active until it succeeds, then liveness/readiness take over
      startupProbe:
        httpGet:
          path: /health
          port: 8000
        failureThreshold: 30      # 30 * 10s = 5 minutes to start
        periodSeconds: 10

      # LIVENESS PROBE — restart container if unhealthy
      # answers: "is the application running properly?"
      livenessProbe:
        httpGet:
          path: /health
          port: 8000
          httpHeaders:
            - name: X-Health-Check
              value: "true"
        initialDelaySeconds: 15    # wait before first check
        periodSeconds: 30          # check every 30 seconds
        timeoutSeconds: 10         # fail if no response in 10s
        successThreshold: 1        # 1 success to mark healthy
        failureThreshold: 3        # 3 failures to restart

      # READINESS PROBE — remove from service endpoints if unhealthy
      # answers: "is the application ready to receive traffic?"
      readinessProbe:
        httpGet:
          path: /ready
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 10
        failureThreshold: 3

      # TCP probe — just checks if port is open
      livenessProbe:
        tcpSocket:
          port: 5432
        initialDelaySeconds: 15
        periodSeconds: 20

      # Exec probe — runs a command inside the container
      livenessProbe:
        exec:
          command:
            - python
            - -c
            - "import requests; requests.get('http://localhost:8000/health')"
        initialDelaySeconds: 15
        periodSeconds: 30
```

---

## 28. Logging in Kubernetes

```bash
# basic pod logs
kubectl logs pod/finsaight-api-xxx
kubectl logs -f pod/finsaight-api-xxx         # follow
kubectl logs --tail=100 pod/finsaight-api-xxx
kubectl logs --since=1h pod/finsaight-api-xxx

# logs from all pods in a deployment (using label selector)
kubectl logs -l app=finsaight -n production
kubectl logs -l app=finsaight --prefix --max-log-requests=10

# previous container logs (crashed container)
kubectl logs --previous pod/finsaight-api-xxx

# multi-container pod
kubectl logs pod/finsaight-api-xxx -c api
kubectl logs pod/finsaight-api-xxx -c log-shipper
```

### Centralized Logging Stack

```yaml
# Elasticsearch + Fluentd + Kibana (EFK stack)
# fluentd daemonset collects logs from all pods
# sends to Elasticsearch
# Kibana provides search and visualization

# Deploy with:
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/master/cluster/addons/fluentd-elasticsearch/fluentd-es-configmap.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kubernetes/master/cluster/addons/fluentd-elasticsearch/fluentd-es-ds.yaml
```

---

## 29. Monitoring with Prometheus and Grafana

```bash
# install kube-prometheus-stack (Prometheus + Grafana + AlertManager)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace \
    --set grafana.adminPassword=admin123 \
    --set prometheus.prometheusSpec.retention=15d

# access Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
# open http://localhost:3000, login admin/admin123

# access Prometheus
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring
```

```yaml
# expose custom metrics from your app
# add to your Service:
apiVersion: v1
kind: Service
metadata:
  name: finsaight-api-svc
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/path: "/metrics"
    prometheus.io/port: "8000"
```

---

# PART 7 — SECURITY

---

## 30. RBAC — Role-Based Access Control

```yaml
# role.yaml — permissions within a namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
  - apiGroups: [""]                # "" = core API group
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "update", "patch"]
```

```yaml
# rolebinding.yaml — bind role to user/group/serviceaccount
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
  - kind: User
    name: jane
    apiGroup: rbac.authorization.k8s.io
  - kind: Group
    name: developers
    apiGroup: rbac.authorization.k8s.io
  - kind: ServiceAccount
    name: my-service-account
    namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

```yaml
# clusterrole.yaml — permissions across ALL namespaces
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-readonly
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["get", "list", "watch"]
```

---

## 31. ServiceAccounts

ServiceAccounts provide an identity for processes running in pods.

```yaml
# serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: finsaight-sa
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/finsaight-role
    # AWS IAM Roles for Service Accounts (IRSA)

# use in pod
spec:
  serviceAccountName: finsaight-sa
```

---

## 32. Pod Security

```yaml
# pod security context
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault

  containers:
    - name: api
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true       # container can't write to /
        capabilities:
          drop:
            - ALL                          # drop all Linux capabilities
          add:
            - NET_BIND_SERVICE            # add back only what's needed

      volumeMounts:
        - name: tmp                        # allow writes to /tmp
          mountPath: /tmp
        - name: cache                      # allow writes to cache
          mountPath: /app/.cache

  volumes:
    - name: tmp
      emptyDir: {}
    - name: cache
      emptyDir: {}
```

---

# PART 8 — ADVANCED TOPICS

---

## 33. Helm — Package Manager for Kubernetes

Helm is the package manager for Kubernetes. A Helm **chart** is a package of pre-configured Kubernetes resources.

```bash
# install Helm
brew install helm                  # Mac
# or: https://helm.sh/docs/intro/install/

# add repositories
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update                   # refresh repository index

# search for charts
helm search repo nginx
helm search hub postgresql         # search on Artifact Hub

# install a chart
helm install my-nginx ingress-nginx/ingress-nginx
helm install my-postgres bitnami/postgresql \
    --set auth.postgresPassword=mysecretpassword \
    --set primary.persistence.size=20Gi \
    --namespace database \
    --create-namespace

# list releases
helm list
helm list -A                       # all namespaces

# upgrade a release
helm upgrade my-postgres bitnami/postgresql \
    --set auth.postgresPassword=mysecretpassword

# rollback
helm rollback my-postgres 1        # rollback to revision 1

# uninstall
helm uninstall my-nginx

# show chart values
helm show values bitnami/postgresql

# override values with file
helm install my-app ./my-chart -f values.yaml -f values.prod.yaml
```

### Creating a Helm Chart

```bash
# create chart structure
helm create finsaight
```

```
finsaight/
├── Chart.yaml           ← chart metadata
├── values.yaml          ← default configuration values
├── charts/              ← chart dependencies
└── templates/           ← Kubernetes manifests with templating
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    ├── _helpers.tpl     ← template helpers
    └── NOTES.txt        ← post-install instructions
```

```yaml
# Chart.yaml
apiVersion: v2
name: finsaight
description: Fins'AIght ML Pipeline
type: application
version: 1.0.0
appVersion: "2.0"
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
```

```yaml
# values.yaml — default values
replicaCount: 3
image:
  repository: kempsly/finsaight-api
  tag: "1.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  host: api.finsaight.example.com

resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

```yaml
# templates/deployment.yaml — Go template syntax
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "finsaight.fullname" . }}
  labels:
    {{- include "finsaight.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "finsaight.selectorLabels" . | nindent 6 }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

---

## 34. Kustomize — Configuration Management

Kustomize lets you customize Kubernetes YAML without templates, using patches and overlays.

```
k8s/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── development/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── production/
        ├── kustomization.yaml
        └── replica-patch.yaml
```

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
commonLabels:
  app: finsaight
```

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
bases:
  - ../../base
namespace: production
images:
  - name: kempsly/finsaight-api
    newTag: "2.0"
patches:
  - path: replica-patch.yaml
```

```yaml
# overlays/production/replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: finsaight-api
spec:
  replicas: 5
```

```bash
# preview what will be applied
kubectl kustomize overlays/production

# apply
kubectl apply -k overlays/production

# diff (what would change)
kubectl diff -k overlays/production
```

---

## 35. Custom Resource Definitions

CRDs extend the Kubernetes API with custom resource types.

```yaml
# crd.yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: mlmodels.finsaight.natixis.com
spec:
  group: finsaight.natixis.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                modelName:
                  type: string
                framework:
                  type: string
                  enum: [xgboost, pytorch, tensorflow, sklearn]
                replicas:
                  type: integer
                  minimum: 1
  scope: Namespaced
  names:
    plural: mlmodels
    singular: mlmodel
    kind: MLModel
```

```yaml
# custom resource instance
apiVersion: finsaight.natixis.com/v1
kind: MLModel
metadata:
  name: credit-default-model
spec:
  modelName: credit-default-xgboost
  framework: xgboost
  replicas: 3
```

---

# PART 9 — ML ON KUBERNETES

---

## 36. Deploying ML Models on Kubernetes

```yaml
# ml-deployment.yaml — complete ML model serving setup
apiVersion: apps/v1
kind: Deployment
metadata:
  name: credit-default-model
  namespace: ml-production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: credit-default-model
  template:
    metadata:
      labels:
        app: credit-default-model
    spec:
      initContainers:
        # init container downloads model before main container starts
        - name: model-downloader
          image: amazon/aws-cli:latest
          command:
            - aws
            - s3
            - cp
            - s3://finsaight-models/credit-default/v2/model.pkl
            - /models/model.pkl
          volumeMounts:
            - name: model-storage
              mountPath: /models
          env:
            - name: AWS_DEFAULT_REGION
              value: eu-west-1

      containers:
        - name: model-server
          image: kempsly/ml-model-server:1.0
          ports:
            - containerPort: 8000
          env:
            - name: MODEL_PATH
              value: /models/model.pkl
            - name: WORKERS
              value: "4"
          resources:
            requests:
              memory: "2Gi"
              cpu: "1000m"
            limits:
              memory: "4Gi"
              cpu: "2000m"
          volumeMounts:
            - name: model-storage
              mountPath: /models
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 30

      volumes:
        - name: model-storage
          emptyDir:
            medium: Memory         # fast in-memory storage for model
            sizeLimit: 2Gi
```

---

## 37. Deploying FastAPI + XGBoost on Kubernetes

### Complete Production Setup

```yaml
# namespace
---
apiVersion: v1
kind: Namespace
metadata:
  name: finsaight

# configmap
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
  namespace: finsaight
data:
  PORT: "8000"
  WORKERS: "4"
  LOG_LEVEL: "info"
  MODEL_PATH: "/app/models/model.ubj"

# secret
---
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
  namespace: finsaight
type: Opaque
stringData:
  groq-api-key: "your-groq-key"
  langsmith-api-key: "your-langsmith-key"

# PVC for models
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ml-models-pvc
  namespace: finsaight
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

# deployment
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: finsaight-api
  namespace: finsaight
  annotations:
    kubernetes.io/change-cause: "Initial deployment v1.0"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: finsaight-api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: finsaight-api
    spec:
      serviceAccountName: finsaight-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
      containers:
        - name: api
          image: kempsly/finsaight-api:1.0
          imagePullPolicy: Always
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: api-config
            - secretRef:
                name: api-secrets
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "2000m"
          volumeMounts:
            - name: models
              mountPath: /app/models
          startupProbe:
            httpGet:
              path: /health
              port: 8000
            failureThreshold: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 30
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: false
      volumes:
        - name: models
          persistentVolumeClaim:
            claimName: ml-models-pvc

# service
---
apiVersion: v1
kind: Service
metadata:
  name: finsaight-api-svc
  namespace: finsaight
spec:
  selector:
    app: finsaight-api
  ports:
    - port: 80
      targetPort: 8000

# HPA
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: finsaight-api-hpa
  namespace: finsaight
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: finsaight-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70

# ingress
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: finsaight-ingress
  namespace: finsaight
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  rules:
    - host: api.finsaight.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: finsaight-api-svc
                port:
                  number: 80
```

```bash
# deploy everything
kubectl apply -f k8s/

# watch rollout
kubectl rollout status deployment/finsaight-api -n finsaight

# test
kubectl port-forward svc/finsaight-api-svc 8080:80 -n finsaight
curl http://localhost:8080/health
```

---

# PART 10 — DEPLOYMENT ON EVERY PLATFORM

---

## 38. Local — Minikube

Minikube runs a single-node Kubernetes cluster inside a VM or container on your local machine. Best for learning and development.

```bash
# ── Install ───────────────────────────────────────────────────
# Mac
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Windows
winget install Kubernetes.minikube

# ── Start cluster ─────────────────────────────────────────────
minikube start
minikube start --driver=docker        # use Docker as driver
minikube start --driver=hyperkit      # use Hyperkit (Mac)
minikube start --cpus=4 --memory=8192 # 4 CPUs, 8GB RAM
minikube start --kubernetes-version=v1.28.0
minikube start --nodes=3              # multi-node cluster

# ── Status and info ───────────────────────────────────────────
minikube status
minikube ip                           # cluster IP
minikube dashboard                    # open web dashboard

# ── Addons ────────────────────────────────────────────────────
minikube addons list
minikube addons enable ingress        # nginx ingress controller
minikube addons enable metrics-server # for HPA
minikube addons enable dashboard      # Kubernetes dashboard
minikube addons enable storage-provisioner

# ── Use local Docker images (no registry needed) ──────────────
eval $(minikube docker-env)           # point Docker CLI to Minikube's Docker
docker build -t finsaight-api:1.0 .  # build directly in Minikube
kubectl apply -f deployment.yaml     # imagePullPolicy: Never

# ── Load local image into Minikube ────────────────────────────
minikube image load finsaight-api:1.0
# or
minikube cache add finsaight-api:1.0

# ── Access services ───────────────────────────────────────────
minikube service finsaight-api-svc    # open service in browser
minikube service finsaight-api-svc --url  # get URL

minikube tunnel                       # enable LoadBalancer services on Mac

# ── Multiple clusters ─────────────────────────────────────────
minikube start -p cluster2            # create named cluster
minikube profile list
minikube profile cluster2

# ── Stop and delete ───────────────────────────────────────────
minikube stop
minikube delete
minikube delete --all

# ── SSH into node ─────────────────────────────────────────────
minikube ssh
```

---

## 39. Local — Kind (Kubernetes in Docker)

Kind runs Kubernetes nodes as Docker containers. Faster than Minikube and better for CI/CD testing.

```bash
# ── Install ───────────────────────────────────────────────────
# Mac
brew install kind

# Linux
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# ── Create cluster ────────────────────────────────────────────
kind create cluster
kind create cluster --name finsaight

# with config file
kind create cluster --config kind-config.yaml
```

```yaml
# kind-config.yaml — multi-node cluster
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:               # forward ports from host to container
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
  - role: worker
  - role: worker
  - role: worker
```

```bash
# list clusters
kind get clusters

# get kubeconfig
kind get kubeconfig --name finsaight

# load local image into Kind (no registry needed)
kind load docker-image finsaight-api:1.0 --name finsaight

# install ingress for Kind
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# delete cluster
kind delete cluster --name finsaight
```

---

## 40. Local — k3s (Lightweight Kubernetes)

k3s is a lightweight Kubernetes distribution. Perfect for edge computing, IoT, and resource-constrained environments. Uses ~512MB RAM.

```bash
# ── Install on Linux/Mac ──────────────────────────────────────
curl -sfL https://get.k3s.io | sh -

# with options
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--no-deploy traefik" sh -

# ── Status ────────────────────────────────────────────────────
sudo k3s kubectl get nodes
sudo systemctl status k3s

# ── kubeconfig ────────────────────────────────────────────────
sudo cat /etc/rancher/k3s/k3s.yaml
# copy to ~/.kube/config, replace 127.0.0.1 with server IP for remote access

# ── Add worker nodes ──────────────────────────────────────────
# on server, get token:
sudo cat /var/lib/rancher/k3s/server/node-token

# on worker node:
curl -sfL https://get.k3s.io | K3S_URL=https://SERVER_IP:6443 K3S_TOKEN=TOKEN sh -

# ── Uninstall ─────────────────────────────────────────────────
/usr/local/bin/k3s-uninstall.sh
```

---

## 41. AWS — Amazon EKS

EKS (Elastic Kubernetes Service) is AWS's managed Kubernetes service.

```bash
# ── Prerequisites ─────────────────────────────────────────────
# install AWS CLI
brew install awscli
aws configure                          # set access key, secret, region

# install eksctl (EKS cluster management tool)
brew install eksctl

# install kubectl
brew install kubectl

# ── Create EKS cluster ────────────────────────────────────────
# simple cluster (takes 15-20 minutes)
eksctl create cluster \
    --name finsaight-cluster \
    --region eu-west-1 \
    --nodegroup-name workers \
    --node-type m5.xlarge \
    --nodes 3 \
    --nodes-min 2 \
    --nodes-max 10 \
    --managed \
    --with-oidc \
    --ssh-access \
    --ssh-public-key my-key
```

```yaml
# cluster.yaml — full cluster configuration
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: finsaight-cluster
  region: eu-west-1
  version: "1.28"

iam:
  withOIDC: true               # enable IAM Roles for Service Accounts

managedNodeGroups:
  # general purpose nodes
  - name: general
    instanceType: m5.xlarge
    desiredCapacity: 3
    minSize: 2
    maxSize: 10
    volumeSize: 100
    ssh:
      allow: true
      publicKeyName: my-key
    iam:
      attachPolicyARNs:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
    labels:
      node-type: general

  # GPU nodes for ML training
  - name: gpu-workers
    instanceType: p3.2xlarge      # NVIDIA V100 GPU
    desiredCapacity: 0            # start with 0, scale on demand
    minSize: 0
    maxSize: 5
    volumeSize: 200
    labels:
      node-type: gpu
    taints:
      - key: nvidia.com/gpu
        value: "true"
        effect: NoSchedule        # only GPU-tolerating pods go here

addons:
  - name: vpc-cni
    version: latest
  - name: coredns
    version: latest
  - name: kube-proxy
    version: latest
  - name: aws-ebs-csi-driver     # for PersistentVolumes with EBS
    version: latest
    wellKnownPolicies:
      ebsCSIController: true

cloudWatch:
  clusterLogging:
    enable: [api, audit, authenticator, controllerManager, scheduler]
```

```bash
# create from config file
eksctl create cluster -f cluster.yaml

# update kubeconfig
aws eks update-kubeconfig --name finsaight-cluster --region eu-west-1

# verify
kubectl get nodes
kubectl get nodes -o wide

# ── IAM Roles for Service Accounts (IRSA) ────────────────────
# allow pods to access AWS services without hardcoding credentials
eksctl create iamserviceaccount \
    --name finsaight-sa \
    --namespace finsaight \
    --cluster finsaight-cluster \
    --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess \
    --approve \
    --override-existing-serviceaccounts

# ── AWS Load Balancer Controller ──────────────────────────────
# required for LoadBalancer services and Ingress with ALB
helm repo add eks https://aws.github.io/eks-charts
helm repo update

eksctl create iamserviceaccount \
    --cluster finsaight-cluster \
    --namespace kube-system \
    --name aws-load-balancer-controller \
    --attach-policy-arn arn:aws:iam::ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
    --approve

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
    -n kube-system \
    --set clusterName=finsaight-cluster \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-load-balancer-controller

# ── EBS CSI Driver for PersistentVolumes ─────────────────────
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.24"

# create StorageClass for EBS
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-gp3
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
EOF

# ── Cluster Autoscaler ────────────────────────────────────────
# automatically add/remove nodes based on pending pods
helm install cluster-autoscaler autoscaler/cluster-autoscaler \
    --set autoDiscovery.clusterName=finsaight-cluster \
    --set awsRegion=eu-west-1 \
    --namespace kube-system

# ── Useful EKS commands ───────────────────────────────────────
eksctl get cluster
eksctl get nodegroup --cluster finsaight-cluster
eksctl scale nodegroup --cluster finsaight-cluster --name workers --nodes 5
eksctl delete cluster --name finsaight-cluster
```

---

## 42. Google Cloud — GKE

GKE (Google Kubernetes Engine) is Google Cloud's managed Kubernetes service. Considered the most mature managed K8s offering.

```bash
# ── Prerequisites ─────────────────────────────────────────────
# install gcloud CLI
# https://cloud.google.com/sdk/docs/install

gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud config set compute/region europe-west1

# install kubectl via gcloud
gcloud components install kubectl

# ── Create GKE cluster ────────────────────────────────────────
# Autopilot cluster (managed node pools — Google manages everything)
gcloud container clusters create-auto finsaight-cluster \
    --region europe-west1 \
    --release-channel regular

# Standard cluster (you manage nodes)
gcloud container clusters create finsaight-cluster \
    --region europe-west1 \
    --num-nodes 3 \
    --machine-type e2-standard-4 \
    --disk-size 100 \
    --enable-autoscaling \
    --min-nodes 1 \
    --max-nodes 10 \
    --enable-autorepair \
    --enable-autoupgrade \
    --enable-ip-alias \
    --enable-network-policy \
    --workload-pool=YOUR_PROJECT_ID.svc.id.goog    # Workload Identity
```

```yaml
# cluster config for production
# create with: gcloud container clusters create-from-config gke-config.yaml
# (via Terraform or gcloud)

# node pools for different workloads
gcloud container node-pools create gpu-pool \
    --cluster finsaight-cluster \
    --region europe-west1 \
    --machine-type n1-standard-4 \
    --accelerator type=nvidia-tesla-t4,count=1 \
    --num-nodes 0 \
    --enable-autoscaling \
    --min-nodes 0 \
    --max-nodes 5 \
    --node-taints nvidia.com/gpu=present:NoSchedule
```

```bash
# ── Configure kubectl ─────────────────────────────────────────
gcloud container clusters get-credentials finsaight-cluster \
    --region europe-west1

# verify
kubectl get nodes

# ── Workload Identity (GKE equivalent of AWS IRSA) ────────────
# allow pods to use Google Cloud service accounts without key files

# create GCP service account
gcloud iam service-accounts create finsaight-sa \
    --display-name "Fins'AIght Service Account"

# grant GCS access
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member serviceAccount:finsaight-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com \
    --role roles/storage.objectViewer

# link to Kubernetes service account
gcloud iam service-accounts add-iam-policy-binding \
    finsaight-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:YOUR_PROJECT_ID.svc.id.goog[finsaight/finsaight-sa]"

kubectl annotate serviceaccount finsaight-sa \
    --namespace finsaight \
    iam.gke.io/gcp-service-account=finsaight-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

# ── GKE Ingress with Google Cloud Load Balancer ───────────────
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: finsaight-ingress
  annotations:
    kubernetes.io/ingress.class: "gce"
    kubernetes.io/ingress.global-static-ip-name: "finsaight-ip"
    networking.gke.io/managed-certificates: "finsaight-cert"
spec:
  rules:
    - host: api.finsaight.example.com
      http:
        paths:
          - path: /*
            pathType: ImplementationSpecific
            backend:
              service:
                name: finsaight-api-svc
                port:
                  number: 80
EOF

# ── Useful GKE commands ───────────────────────────────────────
gcloud container clusters list
gcloud container clusters describe finsaight-cluster --region europe-west1
gcloud container clusters resize finsaight-cluster --num-nodes 5 --region europe-west1
gcloud container clusters delete finsaight-cluster --region europe-west1
```

---

## 43. Microsoft Azure — AKS

AKS (Azure Kubernetes Service) is Microsoft Azure's managed Kubernetes service.

```bash
# ── Prerequisites ─────────────────────────────────────────────
# install Azure CLI
brew install azure-cli

az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# ── Create resource group ─────────────────────────────────────
az group create \
    --name finsaight-rg \
    --location westeurope

# ── Create AKS cluster ────────────────────────────────────────
az aks create \
    --resource-group finsaight-rg \
    --name finsaight-cluster \
    --node-count 3 \
    --node-vm-size Standard_D4s_v3 \
    --enable-cluster-autoscaler \
    --min-count 2 \
    --max-count 10 \
    --kubernetes-version 1.28.0 \
    --enable-managed-identity \
    --enable-addons monitoring \
    --workspace-resource-id /subscriptions/SUB_ID/resourceGroups/RG/providers/Microsoft.OperationalInsights/workspaces/WS \
    --network-plugin azure \
    --network-policy azure \
    --enable-oidc-issuer \
    --enable-workload-identity \
    --generate-ssh-keys

# ── Add GPU node pool ─────────────────────────────────────────
az aks nodepool add \
    --resource-group finsaight-rg \
    --cluster-name finsaight-cluster \
    --name gpupool \
    --node-count 1 \
    --node-vm-size Standard_NC6s_v3 \
    --node-taints nvidia.com/gpu=present:NoSchedule \
    --enable-cluster-autoscaler \
    --min-count 0 \
    --max-count 5

# ── Configure kubectl ─────────────────────────────────────────
az aks get-credentials \
    --resource-group finsaight-rg \
    --name finsaight-cluster

# verify
kubectl get nodes

# ── Workload Identity (Azure equivalent of AWS IRSA) ──────────
# create managed identity
az identity create \
    --name finsaight-identity \
    --resource-group finsaight-rg

# get identity info
IDENTITY_CLIENT_ID=$(az identity show \
    --name finsaight-identity \
    --resource-group finsaight-rg \
    --query clientId -o tsv)

# grant access to Azure Storage
az role assignment create \
    --assignee $IDENTITY_CLIENT_ID \
    --role "Storage Blob Data Reader" \
    --scope /subscriptions/SUB_ID/resourceGroups/finsaight-rg/providers/Microsoft.Storage/storageAccounts/finsaightstorage

# create federated identity credential
AKS_OIDC_ISSUER=$(az aks show \
    --name finsaight-cluster \
    --resource-group finsaight-rg \
    --query "oidcIssuerProfile.issuerUrl" -o tsv)

az identity federated-credential create \
    --name finsaight-federated \
    --identity-name finsaight-identity \
    --resource-group finsaight-rg \
    --issuer $AKS_OIDC_ISSUER \
    --subject system:serviceaccount:finsaight:finsaight-sa

# annotate Kubernetes service account
kubectl annotate serviceaccount finsaight-sa \
    --namespace finsaight \
    azure.workload.identity/client-id=$IDENTITY_CLIENT_ID

# ── AKS Ingress with Application Gateway ─────────────────────
az aks enable-addons \
    --resource-group finsaight-rg \
    --name finsaight-cluster \
    --addons ingress-appgw \
    --appgw-name finsaight-appgw \
    --appgw-subnet-cidr "10.225.0.0/16"

# ── Useful AKS commands ───────────────────────────────────────
az aks list --resource-group finsaight-rg
az aks show --name finsaight-cluster --resource-group finsaight-rg
az aks scale --name finsaight-cluster --resource-group finsaight-rg --node-count 5
az aks upgrade --name finsaight-cluster --resource-group finsaight-rg --kubernetes-version 1.29.0
az aks delete --name finsaight-cluster --resource-group finsaight-rg --yes
```

---

## 44. DigitalOcean — DOKS

DOKS (DigitalOcean Kubernetes Service) is the simplest managed Kubernetes offering. Great for smaller teams and budgets.

```bash
# ── Prerequisites ─────────────────────────────────────────────
# install doctl
brew install doctl

doctl auth init     # enter your API token

# ── Create cluster ────────────────────────────────────────────
doctl kubernetes cluster create finsaight-cluster \
    --region ams3 \
    --version latest \
    --node-pool "name=workers;size=s-4vcpu-8gb;count=3;auto-scale=true;min-nodes=2;max-nodes=10" \
    --wait

# ── Configure kubectl ─────────────────────────────────────────
doctl kubernetes cluster kubeconfig save finsaight-cluster

# verify
kubectl get nodes

# ── Add node pool ─────────────────────────────────────────────
doctl kubernetes cluster node-pool create finsaight-cluster \
    --name high-memory \
    --size s-8vcpu-16gb \
    --count 2

# ── DigitalOcean Spaces for model storage ─────────────────────
# create bucket
doctl storage bucket create finsaight-models --region ams3

# ── Load Balancer (automatic with LoadBalancer service) ───────
# LoadBalancer services automatically provision DigitalOcean LBs
# annotate for specific features:
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: finsaight-lb
  annotations:
    service.beta.kubernetes.io/do-loadbalancer-name: "finsaight-lb"
    service.beta.kubernetes.io/do-loadbalancer-protocol: "http"
    service.beta.kubernetes.io/do-loadbalancer-healthcheck-path: "/health"
spec:
  type: LoadBalancer
  selector:
    app: finsaight-api
  ports:
    - port: 80
      targetPort: 8000
EOF

# ── Useful DOKS commands ──────────────────────────────────────
doctl kubernetes cluster list
doctl kubernetes cluster get finsaight-cluster
doctl kubernetes cluster delete finsaight-cluster
```

---

## 45. On-Premises — kubeadm

kubeadm is the official tool for bootstrapping a production-grade Kubernetes cluster on your own servers.

```bash
# ── PREREQUISITES (run on ALL nodes) ─────────────────────────

# disable swap (required by Kubernetes)
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# load kernel modules
sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

# configure sysctl
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sudo sysctl --system

# install containerd
sudo apt-get update
sudo apt-get install -y containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

# install kubeadm, kubelet, kubectl
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | \
    sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | \
    sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl     # prevent accidental upgrades

# ── INITIALIZE CONTROL PLANE (run on master node only) ────────
sudo kubeadm init \
    --pod-network-cidr=10.244.0.0/16 \         # Flannel CNI CIDR
    --apiserver-advertise-address=MASTER_IP \   # master node's IP
    --kubernetes-version=v1.28.0 \
    --control-plane-endpoint=MASTER_IP:6443

# set up kubeconfig
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# install CNI plugin (Flannel)
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

# OR install Calico (supports NetworkPolicies)
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml

# verify control plane is ready
kubectl get nodes
kubectl get pods -n kube-system

# ── JOIN WORKER NODES (run on each worker) ────────────────────
# kubeadm init prints this command at the end:
sudo kubeadm join MASTER_IP:6443 \
    --token abc.xyz123 \
    --discovery-token-ca-cert-hash sha256:abc123...

# if you lost the join command, regenerate:
kubeadm token create --print-join-command

# ── ADD INGRESS CONTROLLER ────────────────────────────────────
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-nginx \
    --create-namespace \
    --set controller.service.type=NodePort     # use NodePort for bare metal

# ── ADD LOCAL STORAGE ─────────────────────────────────────────
# local-path-provisioner for development
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml

kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

# ── HIGH AVAILABILITY CONTROL PLANE ──────────────────────────
# for production: 3 control plane nodes + load balancer

# on second control plane node (after init on first):
sudo kubeadm join LOAD_BALANCER_IP:6443 \
    --token abc.xyz \
    --discovery-token-ca-cert-hash sha256:abc123 \
    --control-plane \
    --certificate-key CERT_KEY

# ── CLUSTER UPGRADE ───────────────────────────────────────────
# upgrade control plane
sudo apt-get update
sudo apt-get install -y kubeadm=1.29.0-1.1
sudo kubeadm upgrade plan
sudo kubeadm upgrade apply v1.29.0
sudo apt-get install -y kubelet=1.29.0-1.1 kubectl=1.29.0-1.1
sudo systemctl restart kubelet

# upgrade workers
kubectl drain NODE_NAME --ignore-daemonsets --delete-emptydir-data
# (on worker node:)
sudo apt-get install -y kubeadm=1.29.0-1.1
sudo kubeadm upgrade node
sudo apt-get install -y kubelet=1.29.0-1.1
sudo systemctl restart kubelet
kubectl uncordon NODE_NAME
```

---

# PART 11 — REFERENCE

---

## 46. kubectl — Complete Command Reference

```bash
# ── CLUSTER INFO ──────────────────────────────────────────────
kubectl cluster-info
kubectl version
kubectl version --short
kubectl get nodes
kubectl get nodes -o wide
kubectl describe node NODE_NAME
kubectl top nodes                      # CPU/memory usage (needs metrics-server)

# ── CONTEXTS ──────────────────────────────────────────────────
kubectl config get-contexts
kubectl config current-context
kubectl config use-context CONTEXT
kubectl config set-context --current --namespace=NAMESPACE
kubectl config view

# ── GETTING RESOURCES ─────────────────────────────────────────
kubectl get all                        # pods, services, deployments, replicasets
kubectl get all -n NAMESPACE
kubectl get all --all-namespaces       # across all namespaces (-A short form)

kubectl get pods
kubectl get pods -o wide               # show node, IP, nominated node
kubectl get pods -o yaml               # full YAML
kubectl get pods -o json               # full JSON
kubectl get pods -w                    # watch for changes
kubectl get pods -l app=finsaight      # filter by label
kubectl get pods --field-selector status.phase=Running

kubectl get deployments
kubectl get services
kubectl get configmaps
kubectl get secrets
kubectl get pv
kubectl get pvc
kubectl get ingress
kubectl get hpa
kubectl get jobs
kubectl get cronjobs
kubectl get serviceaccounts
kubectl get roles
kubectl get rolebindings
kubectl get clusterroles
kubectl get clusterrolebindings
kubectl get namespaces
kubectl get events                     # cluster events
kubectl get events --sort-by=.lastTimestamp  # sorted

# ── CREATING/APPLYING RESOURCES ───────────────────────────────
kubectl apply -f FILE.yaml             # create or update
kubectl apply -f DIRECTORY/            # apply all YAML in directory
kubectl apply -f https://URL           # apply from URL
kubectl apply -k DIRECTORY/            # apply Kustomization

kubectl create -f FILE.yaml            # create only (fails if exists)
kubectl create namespace NAME
kubectl create configmap NAME --from-literal=key=value
kubectl create secret generic NAME --from-literal=key=value
kubectl create deployment NAME --image=IMAGE
kubectl create service clusterip NAME --tcp=80:8000

# ── UPDATING RESOURCES ────────────────────────────────────────
kubectl edit deployment DEPLOY_NAME    # open in $EDITOR
kubectl set image deployment/NAME container=IMAGE:TAG
kubectl scale deployment NAME --replicas=5
kubectl patch deployment NAME -p '{"spec":{"replicas":3}}'
kubectl annotate deployment NAME kubernetes.io/change-cause="reason"
kubectl label pod NAME new-label=value
kubectl label pod NAME existing-label-     # remove label

# ── DELETING RESOURCES ────────────────────────────────────────
kubectl delete -f FILE.yaml
kubectl delete pod NAME
kubectl delete deployment NAME
kubectl delete namespace NAME          # deletes ALL resources in namespace
kubectl delete all -l app=finsaight    # delete by label selector
kubectl delete all --all               # delete all resources in current namespace

# force delete (for stuck terminating pods)
kubectl delete pod NAME --force --grace-period=0

# ── ROLLOUTS ──────────────────────────────────────────────────
kubectl rollout status deployment/NAME
kubectl rollout history deployment/NAME
kubectl rollout history deployment/NAME --revision=2
kubectl rollout undo deployment/NAME
kubectl rollout undo deployment/NAME --to-revision=2
kubectl rollout pause deployment/NAME
kubectl rollout resume deployment/NAME
kubectl rollout restart deployment/NAME

# ── DEBUGGING ─────────────────────────────────────────────────
kubectl describe pod NAME              # events and status
kubectl describe deployment NAME
kubectl describe node NAME
kubectl describe service NAME

kubectl logs POD_NAME
kubectl logs POD_NAME -c CONTAINER     # specific container
kubectl logs -f POD_NAME               # follow
kubectl logs --previous POD_NAME       # crashed container logs
kubectl logs -l app=finsaight          # all pods matching label

kubectl exec -it POD_NAME -- bash
kubectl exec -it POD_NAME -c CONTAINER -- bash
kubectl exec POD_NAME -- env           # list env vars
kubectl exec POD_NAME -- ls /app

kubectl cp POD_NAME:/remote/path ./local/path
kubectl cp ./local/path POD_NAME:/remote/path

kubectl port-forward pod/POD_NAME 8080:8000
kubectl port-forward deployment/DEPLOY_NAME 8080:8000
kubectl port-forward svc/SERVICE_NAME 8080:80

kubectl top pods                       # CPU/memory for pods
kubectl top pods --sort-by=memory
kubectl top nodes

# ── CUSTOM OUTPUT ─────────────────────────────────────────────
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName

kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'

kubectl get pods --sort-by=.metadata.creationTimestamp
kubectl get pods --sort-by=.status.phase

# ── API RESOURCES ─────────────────────────────────────────────
kubectl api-resources                  # list all resource types
kubectl api-resources --namespaced=true   # namespaced resources only
kubectl explain pod                    # documentation for Pod
kubectl explain pod.spec               # documentation for spec field
kubectl explain deployment.spec.strategy
```

---

## 47. Cheat Sheet

```bash
# ── QUICK REFERENCE ───────────────────────────────────────────

# cluster
kubectl get nodes -o wide
kubectl cluster-info
kubectl top nodes

# switch context
kubectl config use-context CONTEXT
kubectl config set-context --current --namespace=NS

# apply everything
kubectl apply -f .
kubectl apply -k overlays/production

# watch resources
kubectl get pods -w
kubectl get pods -A

# debug
kubectl describe pod NAME
kubectl logs -f NAME
kubectl exec -it NAME -- bash
kubectl events --sort-by=lastTimestamp

# scale
kubectl scale deploy NAME --replicas=5
kubectl autoscale deploy NAME --min=2 --max=10 --cpu-percent=70

# update image
kubectl set image deploy/NAME container=image:tag
kubectl rollout status deploy/NAME
kubectl rollout undo deploy/NAME

# cleanup
kubectl delete pod NAME --force --grace-period=0
kubectl delete all -l app=NAME

# port forward
kubectl port-forward svc/NAME 8080:80

# ── YAML QUICK TEMPLATES ──────────────────────────────────────

# generate YAML without creating:
kubectl create deployment NAME --image=IMAGE --dry-run=client -o yaml > deploy.yaml
kubectl create service clusterip NAME --tcp=80:8000 --dry-run=client -o yaml > svc.yaml
kubectl create configmap NAME --from-literal=key=value --dry-run=client -o yaml > cm.yaml
kubectl create secret generic NAME --from-literal=key=val --dry-run=client -o yaml > secret.yaml

# ── PLATFORM QUICKSTART ───────────────────────────────────────

# Minikube (local)
minikube start --cpus=4 --memory=8192
minikube addons enable ingress metrics-server
minikube tunnel              # enable LoadBalancer
eval $(minikube docker-env)  # use Minikube's Docker

# Kind (local)
kind create cluster --config kind-config.yaml
kind load docker-image myimage:tag

# EKS (AWS)
eksctl create cluster -f cluster.yaml
aws eks update-kubeconfig --name CLUSTER --region eu-west-1

# GKE (Google)
gcloud container clusters create-auto CLUSTER --region europe-west1
gcloud container clusters get-credentials CLUSTER --region europe-west1

# AKS (Azure)
az aks create -g RG -n CLUSTER --node-count 3
az aks get-credentials -g RG -n CLUSTER

# DOKS (DigitalOcean)
doctl kubernetes cluster create CLUSTER --region ams3
doctl kubernetes cluster kubeconfig save CLUSTER

# kubeadm (on-prem)
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

# ── KEY CONCEPTS ──────────────────────────────────────────────
# Pod           = one or more containers, same network/storage
# Deployment    = manages Pod replicas, rolling updates
# Service       = stable endpoint for Pods (ClusterIP/NodePort/LB)
# ConfigMap     = non-sensitive configuration
# Secret        = sensitive data (base64 encoded)
# PVC           = request for persistent storage
# Ingress       = HTTP routing and TLS termination
# HPA           = auto-scale pods based on metrics
# Namespace     = logical isolation within cluster
# StatefulSet   = for databases, stable identities
# DaemonSet     = one pod per node
# Job/CronJob   = run-to-completion / scheduled tasks
```

---

*Kubernetes docs: https://kubernetes.io/docs*  
*kubectl reference: https://kubernetes.io/docs/reference/kubectl*  
*Helm: https://helm.sh/docs*  
*EKS docs: https://docs.aws.amazon.com/eks*  
*GKE docs: https://cloud.google.com/kubernetes-engine/docs*  
*AKS docs: https://docs.microsoft.com/en-us/azure/aks*  
*DOKS docs: https://docs.digitalocean.com/products/kubernetes*  
*kubeadm docs: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm*  
*Kubernetes the Hard Way: https://github.com/kelseyhightower/kubernetes-the-hard-way*
