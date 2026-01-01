# UFC Web Scrapper Helm Chart

This Helm chart deploys the UFC Web Scrapper application stack including:
- MySQL database with persistent storage
- Python web scrapper service
- Node.js API service
- Optional Ingress configuration

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- PV provisioner support in the underlying infrastructure (for MySQL persistence)

## Installing the Chart

To install the chart with the release name `ufc-webscrapper`:

```bash
helm install ufc-webscrapper ./helm-chart
```

To install with custom values:

```bash
helm install ufc-webscrapper ./helm-chart -f custom-values.yaml
```

## Uninstalling the Chart

```bash
helm uninstall ufc-webscrapper
```

## Configuration

The following table lists the configurable parameters and their default values.

### MySQL Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `mysql.enabled` | Enable MySQL deployment | `true` |
| `mysql.image.repository` | MySQL image repository | `edthegreat/ufc_mysql_db` |
| `mysql.image.tag` | MySQL image tag | `4` |
| `mysql.rootPassword` | MySQL root password | `password` |
| `mysql.database` | MySQL database name | `mysql01` |
| `mysql.user` | MySQL user | `mysqluser` |
| `mysql.password` | MySQL password | `password` |
| `mysql.service.type` | MySQL service type | `LoadBalancer` |
| `mysql.service.port` | MySQL service port | `3306` |
| `mysql.persistence.enabled` | Enable persistence | `true` |
| `mysql.persistence.size` | PVC size | `1Gi` |
| `mysql.persistence.storageClass` | Storage class | `local-storage` |
| `mysql.persistence.hostPath` | Host path for PV | `/mnt/data` |

### Python Web Scrapper Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `pythonWebscrapper.enabled` | Enable Python scrapper | `true` |
| `pythonWebscrapper.image.repository` | Image repository | `edthegreat/ufc_python_webscrapper` |
| `pythonWebscrapper.image.tag` | Image tag | `13` |
| `pythonWebscrapper.replicas` | Number of replicas | `1` |

### Node.js API Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `nodejsApi.enabled` | Enable Node.js API | `true` |
| `nodejsApi.image.repository` | Image repository | `edthegreat/ufc_nodejs_api` |
| `nodejsApi.image.tag` | Image tag | `5` |
| `nodejsApi.replicas` | Number of replicas | `1` |
| `nodejsApi.service.type` | Service type | `LoadBalancer` |
| `nodejsApi.service.port` | Service port | `3000` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class name | `ngrok` |
| `ingress.host` | Ingress host | `nice-mongrel-choice.ngrok-free.app` |

## Examples

### Deploy with custom image tags

```bash
helm install ufc-webscrapper ./helm-chart \
  --set mysql.image.tag=5 \
  --set pythonWebscrapper.image.tag=14 \
  --set nodejsApi.image.tag=6
```

### Deploy without Python scrapper

```bash
helm install ufc-webscrapper ./helm-chart \
  --set pythonWebscrapper.enabled=false
```

### Enable Ingress

```bash
helm install ufc-webscrapper ./helm-chart \
  --set ingress.enabled=true \
  --set ingress.host=your-domain.com
```

### Upgrade with new values

```bash
helm upgrade ufc-webscrapper ./helm-chart -f new-values.yaml
```

## Accessing the Application

After installation, get the service URLs:

```bash
# Get MySQL service
kubectl get svc ufc-webscrapper-mysql

# Get Node.js API service
kubectl get svc ufc-webscrapper-nodejs-api
```

## Troubleshooting

Check pod status:
```bash
kubectl get pods -l app.kubernetes.io/name=ufc-webscrapper
```

View logs:
```bash
kubectl logs -l app.kubernetes.io/component=mysql
kubectl logs -l app.kubernetes.io/component=python-webscrapper
kubectl logs -l app.kubernetes.io/component=nodejs-api
```
