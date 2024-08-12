from typing import Annotated, Optional

import typer

app = typer.Typer(no_args_is_help=True)


@app.command("publish")
def publish(
    strict_mode: Annotated[Optional[bool], typer.Option(help="Whether the app should run in strict mode")] = False,
    kafka_host: Annotated[Optional[str], typer.Argument(help="Host address of Kafka")] = None,
    kafka_port: Annotated[Optional[int], typer.Argument(help="Port of Kafka")] = None,
):
    print(f"Running in {strict_mode=}")
    print(f"[{kafka_host}:{kafka_port}]")


if __name__ == "__main__":
    app()
