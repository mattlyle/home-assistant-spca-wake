@echo off

echo Using container: %1

docker exec -it -u root %1 mkdir /workspaces/homeassistant-core/homeassistant/components/spca_wake

docker cp custom_components/spca_wake/spca_wake_web.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/__init__.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/config_flow.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/coordinator.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/const.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/manifest.json %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/sensor.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/strings.json %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/translations/en.json %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/translations/

docker exec -it -u root %1 chown vscode:vscode -R /workspaces/homeassistant-core/homeassistant/components/spca_wake

docker exec -it %1 ls -lah /workspaces/homeassistant-core/homeassistant/components/spca_wake
