@echo off

echo Using container: %1

docker cp wake_spca/wake_spca.py %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/
docker cp wake_spca/__init__.py %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/
docker cp wake_spca/config_flow.py %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/
docker cp wake_spca/coordinator.py %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/
docker cp wake_spca/const.py %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/
docker cp wake_spca/manifest.json %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/
docker cp wake_spca/sensor.py %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/
docker cp wake_spca/strings.json %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/
docker cp wake_spca/translations/en.json %1:/workspaces/homeassistant-core/homeassistant/components/wake_spca/translations/

docker exec -it -u root %1 chown vscode:vscode -R /workspaces/homeassistant-core/homeassistant/components/wake_spca

docker exec -it %1 ls -lah /workspaces/homeassistant-core/homeassistant/components/wake_spca
