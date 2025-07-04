import requests, uuid, traceback
from report_utils import generate_pdf_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def delete_user(user_id: int) -> None:
    r = requests.delete(f"{USERS_URL}/{user_id}")
    assert r.status_code == 200, "User deletion failed"
    # comprobar que ya no existe
    assert requests.get(f"{USERS_URL}/{user_id}").status_code == 404, \
           "User still present after deletion"
    print(f"User {user_id} deleted and verified")

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def delete_task(task_id: int) -> None:
    r = requests.delete(f"{TASKS_URL}/{task_id}")
    assert r.status_code == 200, "Task deletion failed"
    # comprobar que ya no existe
    assert requests.get(f"{TASKS_URL}/{task_id}").status_code == 404, \
           "Task still present after deletion"
    print(f"Task {task_id} deleted and verified")

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def integration_test():

    baseline_users = {u["id"] for u in requests.get(USERS_URL).json()}
    baseline_tasks = {t["id"] for t in requests.get(TASKS_URL).json()}

    results = []

    user_id = task_id = None   # para poder limpiar en finally

    try:
        user_id = create_user("Camilo")
        results.append(("create_user", True, None))

        task_id = create_task(user_id, "Prepare presentation")
        results.append(("create_task", True, None))

        ok = any(t["id"] == task_id and t["user_id"] == user_id for t in get_tasks())
        results.append(("task_registered", ok, None if ok else "not found"))
        assert ok

    except Exception as e:
        results.append(("exception", False, str(e)))
        traceback.print_exc()

    finally:
    # borrado de task
        if task_id and task_id not in baseline_tasks:
            try:
                delete_task(task_id)
                results.append((f"delete_task_{task_id}", True, None))
            except Exception as e:
                results.append((f"delete_task_{task_id}", False, str(e)))

    # borrado de user
    if user_id and user_id not in baseline_users:
        try:
            delete_user(user_id)
            results.append((f"delete_user_{user_id}", True, None))
        except Exception as e:
            results.append((f"delete_user_{user_id}", False, str(e)))

    # verificación global
    same_users = {u["id"] for u in requests.get(USERS_URL).json()} == baseline_users
    same_tasks = {t["id"] for t in requests.get(TASKS_URL).json()} == baseline_tasks
    results.append(("global_users_ok",  same_users, None if same_users else "mismatch"))
    results.append(("global_tasks_ok",  same_tasks, None if same_tasks else "mismatch"))

    generate_pdf_report("BackEnd-Test", results)


if __name__ == "__main__":
    integration_test()