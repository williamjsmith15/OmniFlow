import docker



client = docker.from_env()
toilContainer = client.containers.get("omniflow-openmc-1")

var = toilContainer.exec_run(["python", "OmniFlow/ToilRunner/test_in_a_test.py"])

print(var[1])
