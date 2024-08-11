## Module 2

Explored topics:
- Data Storage
- Data Labeling

## Configure MinIO

Install dependencies

```bash
pip install -r requirements.txt
```

Run with Docker

```bash
docker run -it -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ":9001"
```

Run with K8S

```bash
kubectl create -f .k8s/minio.yaml
kubectl port-forward --address=0.0.0.0 pod/minio 9000:9000 9001:9001
```