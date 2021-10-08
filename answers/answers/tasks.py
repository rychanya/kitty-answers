import celery
import os

app = celery.Celery("tasker")
# app.conf.update(
#     BROKER_URL=os.environ["REDIS_URL"], CELERY_RESULT_BACKEND=os.environ["REDIS_URL"]
# )
app.conf.broker_url = os.environ["REDIS_URL"]


@app.task
def add(x, y):
    return x + y
