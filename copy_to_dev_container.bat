@echo off

cls

set DOCKER_CLI_HINTS=false

echo Using container: %1

echo.
echo Making sure directories exist...
docker exec -it -u root %1 mkdir -p /workspaces/homeassistant-core/homeassistant/components/spca_wake
docker exec -it -u root %1 mkdir -p /workspaces/homeassistant-core/homeassistant/components/spca_wake/translations

echo.
echo Copying files...
docker cp custom_components/spca_wake/spca_wake_web.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/__init__.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/config_flow.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/coordinator.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/const.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/manifest.json %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/sensor.py %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/strings.json %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/
docker cp custom_components/spca_wake/translations/en.json %1:/workspaces/homeassistant-core/homeassistant/components/spca_wake/translations/

echo.
echo Setting file permissions...
docker exec -it -u root %1 chown vscode:vscode -R /workspaces/homeassistant-core/homeassistant/components/spca_wake

echo.
echo Running hassfest...
docker exec -it -w /workspaces/homeassistant-core %1 python -m script.hassfest

echo.
echo Running gen_requirements_all
docker exec -it -w /workspaces/homeassistant-core %1 python -m script.gen_requirements_all

echo.
echo Verify permissions:
docker exec -it %1 ls -lah /workspaces/homeassistant-core/homeassistant/components/spca_wake
