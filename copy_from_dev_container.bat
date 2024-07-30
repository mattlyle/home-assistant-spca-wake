@echo off

echo Using container: %1

docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/wake_spca.py wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/__init__.py wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/config_flow.py wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/coordinator.py wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/const.py wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/manifest.json wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/sensor.py wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/strings.json wake_spca/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/translations/en.json wake_spca/translations/en.json
