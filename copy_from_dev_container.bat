@echo off

echo Using container: %1

docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/wake_spca.py custom_components/wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/__init__.py custom_components/wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/config_flow.py custom_components/wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/coordinator.py custom_components/wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/const.py custom_components/wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/manifest.json custom_components/wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/sensor.py custom_components/wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/strings.json custom_components/wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/translations/en.json custom_components/wake_spca/translations/en.json
