echo "Let's set up the application"
echo "Installing dependencies"
pip install -r requirements.txt
echo "Setting up three external volumes for our docker application. These will be used to store the application data, Grafana and the Prometheus data." 

docker volume create \
  --driver local \
  --opt type=none \
  --opt device=./app_data/ \
  --opt o=bind \
  app_data

docker volume create \
  --driver local \
  --opt type=none \
  --opt device=./prometheus_data/ \
  --opt o=bind \
  prometheus_data

docker volume create \
  --driver local \
  --opt type=none \
  --opt device=./grafana_data/ \
  --opt o=bind \
  grafana_data

echo "Setting up the database"
