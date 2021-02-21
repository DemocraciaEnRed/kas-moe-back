from invoke import task

@task
def serve(c):
    c.run("cd src && poetry run uvicorn main:app --reload", pty=True)
