# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""Common tasks for Invoke, a cross-platform replacement for Make"""

from invoke import task

from src.config.defs import package_name
from src.config.glob import ENV_PREFIX


@task(
    default=True,
    help={
        'development': 'run a development server'
    }
)
def serve(ctx, development=False):
    """Run a development or production server."""
    if development:
        ctx.run(
            f'cd {package_name} && uvicorn main:app --reload',
            echo=True,
            pty=True,
            env={
                f'{ENV_PREFIX}ALLOWED_HOSTS': '["127.0.0.1"]',
                f'{ENV_PREFIX}DEVELOPMENT_MODE': 'true',
            }

        )
    else:
        ctx.run(
            f'cd {package_name} && gunicorn --config config/gunicorn.py --pythonpath "$(pwd)"'
            f' main:app',
            echo=True,
        )


@task
def lint(ctx):
    """Run flake8 with proper exclusions."""
    ctx.run(
        f'flake8 {package_name}/',
        echo=True,
    )


@task(
    aliases=['cc'],
    help={
        'complex': 'filter results to show only potentially complex functions (B+)',
    }
)
def cyclomatic_complexity(ctx, complex_=False):
    """Analise code Cyclomatic Complexity using radon."""
    # Run Cyclomatic Complexity
    cmd = 'radon cc -s -a'
    if complex_:
        cmd += ' -nb'
    ctx.run(f'{cmd} {package_name}', pty=True)

