import nox_poetry


@nox_poetry.session(python=["3.9", "3.10", "3.11"])
def tests(session):
    session.install("pytest")
    session.install("pytest-cov")
    session.install(".")

    session.run(
        "pytest",
        "--cov",
    )


@nox_poetry.session
def lint(session):
    session.install("black")
    session.install("blackdoc")
    # session.install("isort")
    session.install("ruff")

    session.run("black", "--check", ".")
    session.run("blackdoc", "--check", ".")
    # session.run("isort", "--check-only", ".")
    session.run("ruff", "check", ".")


@nox_poetry.session
def typing(session):
    session.install("mypy")
    session.run("mypy", "src/gptel", "--namespace-packages", "--ignore-missing-imports")
