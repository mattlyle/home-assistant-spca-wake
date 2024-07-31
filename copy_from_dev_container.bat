@echo off

echo Using container: %1

docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/spca_wake_web.py custom_components/spca_wake/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/__init__.py custom_components/spca_wake/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/config_flow.py custom_components/spca_wake/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/coordinator.py custom_components/spca_wake/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/const.py custom_components/spca_wake/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/manifest.json custom_components/spca_wake/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/sensor.py custom_components/spca_wake/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/strings.json custom_components/spca_wake/
docker cp %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/translations/en.json custom_components/spca_wake/translations/en.json
