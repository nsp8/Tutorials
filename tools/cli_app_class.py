from enum import StrEnum, unique
from typing import Annotated, Optional, Self
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from pydantic import BaseModel, ConfigDict, model_validator
import typer
from utils import reverse_lookup

app = typer.Typer(no_args_is_help=True)
console = Console()
null_params = list()


@unique
class AppState(StrEnum):
    STOPPED = "stopped"
    RUNNING = "running"
    EXITED = "exited"
    TERMINATED = "terminated"


class ParametersAbsentException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class CLIParams(BaseModel):
    strict_mode: bool
    kafka_host: Optional[str] = None
    kafka_port: Optional[int] = None
    kafka_topic: Optional[str] = None
    m_and_v_host: Optional[str] = None
    m_and_v_port: Optional[int] = None
    m_and_v_api_slug: Optional[str] = None
    dispatch_file_path: Optional[str] = None
    meas_file_path: Optional[str] = None
    publish_delay_seconds: Optional[int] = None
    results_delay_seconds: Optional[int] = None
    results_file_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_params(self) -> Self:
        global null_params
        params = self.model_dump()
        params.pop("strict_mode")
        null_params = reverse_lookup(params).get(None)

        if not all(params.values()):
            raise ParametersAbsentException("These user parameters were not present:")
        return self


def prompt_for_params(param_list: list) -> dict:
    filled_params = dict()
    print("Please enter values for these parameters: ")
    while param_list:
        param = param_list.pop(0)
        user_input = typer.prompt(param)
        if user_input:
            filled_params[param] = user_input
    return filled_params


def parse_string_inputs(input_value: Optional[str] = None):
    stripped = input_value.strip()
    if stripped:
        return stripped
    return None


def parse_integer_inputs(input_value: Optional[str] = None):
    if input_value:
        return max(0, int(input_value))
    return None


@app.command("publish")
def main(
        strict_mode: Annotated[bool, typer.Option()] = False,
        kafka_host: Annotated[Optional[str], typer.Argument(parser=parse_string_inputs)] = None,
        kafka_port: Annotated[Optional[int], typer.Argument(parser=parse_integer_inputs)] = None,
        kafka_topic: Annotated[Optional[str], typer.Argument(parser=parse_string_inputs)] = None,
        m_and_v_host: Annotated[Optional[str], typer.Argument(parser=parse_string_inputs)] = None,
        m_and_v_port: Annotated[Optional[int], typer.Argument()] = None,
        m_and_v_api_slug: Annotated[Optional[str], typer.Argument(parser=parse_string_inputs)] = None,
        dispatch_file_path: Annotated[Optional[str], typer.Argument(parser=parse_string_inputs)] = None,
        meas_file_path: Annotated[Optional[str], typer.Argument(parser=parse_string_inputs)] = None,
        publish_delay_seconds: Annotated[Optional[int], typer.Argument()] = None,
        results_delay_seconds: Annotated[Optional[int], typer.Argument()] = None,
        results_file_path: Annotated[Optional[str], typer.Argument(parser=parse_string_inputs)] = None,
        suppress_traceback: Annotated[bool, typer.Option()] = False,
):
    global null_params
    cli_params = None
    try:
        cli_params = CLIParams(
            strict_mode=strict_mode,
            kafka_host=kafka_host,
            kafka_port=kafka_port,
            kafka_topic=kafka_topic,
            m_and_v_host=m_and_v_host,
            m_and_v_port=m_and_v_port,
            m_and_v_api_slug=m_and_v_api_slug,
            dispatch_file_path=dispatch_file_path,
            meas_file_path=meas_file_path,
            publish_delay_seconds=publish_delay_seconds,
            results_delay_seconds=results_delay_seconds,
            results_file_path=results_file_path,
        )
    except ParametersAbsentException as e:
        if not suppress_traceback:
            console.print_exception(show_locals=False)
        print(Panel.fit(f"{e if suppress_traceback else None}\n{null_params}", border_style="red"))
        cli_params = CLIParams(strict_mode=strict_mode, **prompt_for_params(null_params))
    finally:
        pretty = Pretty(cli_params.model_dump())
        panel = Panel(pretty)
        print(panel)


if __name__ == "__main__":
    # typer.run(main)
    app()
