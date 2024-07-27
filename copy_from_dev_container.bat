@echo off

echo Using container: %1

docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/wakespca.py wake_spca_status/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/__init__.py wake_spca_status/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/config_flow.py wake_spca_status/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/coordinator.py wake_spca_status/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/const.py wake_spca_status/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/manifest.json wake_spca_status/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/sensor.py wake_spca_status/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/strings.json wake_spca_status/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/translations/en.json wake_spca_status/translations/en.json
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca_status/wakespca.py wake_spca_status/