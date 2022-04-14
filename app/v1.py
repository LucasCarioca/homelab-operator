import kopf
import services.k8s_service as k8s

@kopf.on.create('applications')
async def create_application_controller(name, namespace, spec, logger, **kwargs): 
    logger.info(f"Creating Application: {namespace}/{name}")
    
    container_name = spec.get('containerName')
    container_tag = spec.get('containerTag')
    replicas = spec.get('replicas')
    port = spec.get('port')

    if not container_name or not container_tag:
        raise kopf.PermanentError(f"Container name and tag are required")
    if not name or not namespace:
        raise kopf.PermanentError(f"Application name and namespace are required")
    if not port:
        raise kopf.PermanentError(f"Application port is required")
    if not replicas :
        replicas = 1

    await k8s.create_deployment(name, namespace, container_name, container_tag, replicas, logger)
    await k8s.create_service(name, namespace, port, logger)


@kopf.on.update('applications')
async def update_application_controller(name, namespace, spec, logger, **kwargs): 
    logger.info(f"Updating Application: {namespace}/{name}")
    
    container_name = spec.get('containerName')
    container_tag = spec.get('containerTag')
    replicas = spec.get('replicas')
    port = spec.get('port')

    if not container_name or not container_tag:
        raise kopf.PermanentError(f"Container name and tag are required")
    if not name or not namespace:
        raise kopf.PermanentError(f"Application name and namespace are required")
    if not port:
        raise kopf.PermanentError(f"Application port is required")
    if not replicas :
        replicas = 1

    await k8s.update_deployment(name, namespace, container_name, container_tag, replicas, logger)
    await k8s.update_service(name, namespace, port, logger)