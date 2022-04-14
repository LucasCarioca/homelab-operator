import kopf
import kubernetes
import yaml
from utils import get_template

async def create_deployment(name, namespace, container_name, container_tag, replicas, logger):
    logger.info(f"Creating Deployment: {namespace}/{name}")

    deployment_template = get_template('v1', 'application', 'deployment')
            
    deployment_text = deployment_template.format(
        name=name, 
        namespace=namespace, 
        container_name=container_name, 
        container_tag=container_tag, 
        replicas=replicas)
    deployment = yaml.safe_load(deployment_text)

    kopf.adopt(deployment)

    api=kubernetes.client.AppsV1Api()
    try:
        api.create_namespaced_deployment(namespace=namespace, body=deployment)
    except Exception as e:
        logger.error("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)

async def create_service(name, namespace, port, logger):
    logger.info(f"Creating Service: {namespace}/{name}")

    service_template = get_template('v1', 'application', 'service')
    
    service_text = service_template.format(
        name=name, 
        namespace=namespace, 
        port=port)
    service = yaml.safe_load(service_text)

    kopf.adopt(service)

    api=kubernetes.client.AppsV1Api()
    try:
        api.create_namespaced_service(namespace=namespace, body=service)
    except Exception as e:
        logger.error("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)