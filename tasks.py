# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""Common tasks for Invoke, a cross-platform replacement for Make"""

from invoke import task

from src.conf.defs import package_name


@task(
    default=True,
    help={
        'serve': 'run a development server'
    }
)
def serve(c):
    """Run a development server."""
    c.run("cd src && poetry run uvicorn main:app --reload", pty=True)


@task
def flake8(ctx):
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

