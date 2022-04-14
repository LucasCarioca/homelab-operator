from distutils.command.build import build
import kopf
import kubernetes
import yaml
from utils import get_template


async def create_deployment(name, namespace, container_name, container_tag, replicas, logger):
    logger.info(f"Creating Deployment: {namespace}/{name}")
    doc = build_deployment_file(name, namespace,container_name, container_tag, replicas)
    kopf.adopt(doc)
    api=kubernetes.client.AppsV1Api()
    try:
        api.create_namespaced_deployment(namespace=namespace, body=doc)
    except Exception as e:
        logger.error(f"Exception when calling AppsV1Api->create_namespaced_deployment: {str(e)}")

async def update_deployment(name, namespace, container_name, container_tag, replicas, logger):
    logger.info(f"Updating Deployment: {namespace}/{name}")
    doc = build_deployment_file(name, namespace,container_name, container_tag, replicas)
    kopf.adopt(doc)
    api=kubernetes.client.AppsV1Api()
    try:
        api.patch_namespaced_deployment(name=doc['metadata']['name'], namespace=namespace, body=doc)
    except Exception as e:
        logger.error(f"Exception when calling AppsV1Api->patch_namespaced_deployment: {str(e)}")



async def create_service(name, namespace, port, logger):
    logger.info(f"Create Service: {namespace}/{name}")
    doc = build_service_file(name, namespace, port)
    kopf.adopt(doc)
    api=kubernetes.client.CoreV1Api()
    try:
        api.create_namespaced_service(namespace=namespace, body=doc)
    except Exception as e:
        logger.error(f"Exception when calling CoreV1Api->create_namespaced_service: {str(e)}")


async def update_service(name, namespace, port, logger):
    logger.info(f"Updating Service: {namespace}/{name}")
    doc = build_service_file(name, namespace, port)
    kopf.adopt(doc)
    api=kubernetes.client.CoreV1Api()
    try:
        api.patch_namespaced_service(name=doc['metadata']['name'], namespace=namespace, body=doc)
    except Exception as e:
        logger.error(f"Exception when calling CoreV1Api-patch_namespaced_service: {str(e)}")



def build_deployment_file(name, namespace, container_name, container_tag, replicas):
    deployment_template = get_template('v1', 'application', 'deployment')
    deployment_text = deployment_template.format(
        name=name, 
        namespace=namespace, 
        container_name=container_name, 
        container_tag=container_tag, 
        replicas=replicas)
    return yaml.safe_load(deployment_text)

def build_service_file(name, namespace, port):
    service_template = get_template('v1', 'application', 'service')
    service_text = service_template.format(
        name=name, 
        namespace=namespace, 
        port=port)
    return yaml.safe_load(service_text)