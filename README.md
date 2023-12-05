# namudhaj
Serving LLMs (Falcon 7b instruct, Llama 2 70B, ) with GPUs on Google Kubernetes Engine (GKE)

## Authors
*   Sepehr Ahmadi
*   Zafar Mahmood

## Motivation
Deploying a large language model on Kubernetes with GPUs helps with quick iterative development of NLP tasks and prompt engineering.

With this motivation, we started this project as part of the **ECE1779 Introduction to Cloud Computing** course.


## Installation steps:

1.  Make sure you have enabled Google Kubernetes Engine API.

2. Also enable Container File System API.

3.  If you want to use Llama 2 models, get access to the Meta license as the Llama models are governed by it. Follow the details [here](https://huggingface.co/meta-llama/Llama-2-7b-hf).

4.  Create a HuggingFace token.

5. Set the default environment variables:
```bash
$ source ./gcs_scripts/set_environment.sh

Updated property [core/project].
```

6. Create a cluster named ``llm-cluster``: 
```bash
$ ./gcs_scripts/create_cluster.sh

Creating cluster llm-cluster in us-central1... Cluster is be
ing deployed...⠼
Creating cluster llm-cluster in us-central1... Cluster is be
ing health-checked (master is healthy)...done.
Created [https://container.googleapis.com/v1/projects/ece1779project/zones/us-central1/clusters/llm-cluster].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/us-central1/llm-cluster?project=ece1779project
```

7.  Create a GPU node pool:
```bash
$ ./gcs_scripts/create_gpu_node_pool.sh

Creating node pool g2-standard-24...done.
Created [https://container.googleapis.com/v1/projects/ece1779project/zones/us-central1/clusters/llm-cluster/nodePools/g2-standard-24].
NAME            MACHINE_TYPE    DISK_SIZE_GB  NODE_VERSION
g2-standard-24  g2-standard-24  100           1.27.3-gke.100
```

8.  Install the GKE Auth plugin:
```bash
$ gcloud components install gke-gcloud-auth-plugin
```

9.  Configure kubectl:
```bash
$ gcloud container clusters get-credentials llm-cluster --region=${REGION}

Fetching cluster endpoint and auth data.
kubeconfig entry generated for llm-cluster.
```

10. Set the HuggingFace token. [Here](https://huggingface.co/settings/tokens) is how you get the HuggingFace token:
```bash
$ export HF_TOKEN=HUGGING_FACE_TOKEN
```

11. Create a Kubernetes secret for the HuggingFace token:
```bash
$ ./gcs_scripts/create_hf_k8s_secret.sh
```

12. Apply the manifest:
```
$ kubectl apply -f configs/hf-secret.yaml

secret/llm-cluster created
```

13. Build, tag and push the docker image. [Here](https://hub.docker.com/repository/docker/zaffnet/namudhaj/general) is the DockerHub repository:
```bash
$ ./build.sh
$ docker push 
```

14. Create the text generation interface k8s Deployment (with number of replicas = 1):
```bash
$ kubectl apply -f configs/text-generation-inference.yaml

deployment.apps/llm created
service/llm-service created
```

15. Deploy the frontend Gradio app (both Deployment and Service):
```bash
$ kubectl apply -f configs/gradio-tgi.yaml
```