use_minikube_env:
	eval $(minikube docker-env)
	docker-compose up

minikube_add_images:
	minikube image load docker-mysql
	minikube image load docker-put-info-service
	minikube image load docker-web-service

minikube_run_templates:
	kubectl apply -f kuber/web-service-deployment.yaml
	kubectl apply -f kuber/web-service-ingress.yaml
	kubectl apply -f kuber/web-service-service.yaml


minikube_delete_images:
	minikube image rm docker-mysql
	minikube image rm docker-put-info-service
	minikube image rm docker-web-service
