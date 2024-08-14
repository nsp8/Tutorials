from copy import deepcopy
from typing import Annotated, Optional, Self, Type
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator
import typer
from tools.utils import parse_integer_inputs, parse_string_inputs, reverse_lookup, Parameter, describe_parameters

app = typer.Typer(no_args_is_help=True)
console = Console()
user_params: dict = dict()


class ParametersAbsentException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class CLIParams(BaseModel):
    strict_mode: Parameter
    dispatch_file_path: Optional[Parameter] = None
    meas_file_path: Optional[Parameter] = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def validate_params(self) -> Self:
        global user_params
        params = self.model_dump(mode="python")
        params.pop("strict_mode")
        # user_params = reverse_lookup(params)
        user_params = params
        if None in reverse_lookup(user_params):
            raise ParametersAbsentException("These user parameters were not present:")
        return self


class PublishParams(CLIParams):
    kafka_host: Optional[Parameter] = None
    kafka_port: Optional[Parameter] = None
    kafka_topic: Optional[Parameter] = None
    m_and_v_host: Optional[Parameter] = None
    m_and_v_port: Optional[Parameter] = None
    m_and_v_api_slug: Optional[Parameter] = None
    publish_delay_seconds: Optional[Parameter] = None
    results_delay_seconds: Optional[Parameter] = None
    results_file_path: Optional[Parameter] = None


class VerifyParams(CLIParams):
    ...


def prompt_for_params(parameters: dict[str, Parameter]) -> dict:
    filled_params = deepcopy(parameters)
    print("Please enter values for these parameters: ")
    for name, param in parameters.items():
        if param.value is None:
            filled_params[name] = Parameter(
                name=param.name,
                value=typer.prompt(name),
                required=param.required
            )
    return filled_params


def handle_incomplete_parameters(
        app_mode: Type[PublishParams] | Type[VerifyParams],
        strict_mode: bool,
        suppress_traceback: bool,
        exception: ParametersAbsentException
):
    preamble = f"{exception}\n"
    if not suppress_traceback:
        console.print_exception(show_locals=False)
        preamble = ""
    null_params = reverse_lookup(user_params).get(None)
    print(Panel.fit(f"{preamble}{null_params}", border_style="red"))
    cli_params = None
    try:
        cli_params = app_mode(
            strict_mode=Parameter(name="strict_mode", value=strict_mode),
            **prompt_for_params(user_params)
        )
    except ValidationError as ve:
        print(Panel.fit(ve))
    return cli_params


@app.command()
def publish(
        strict_mode: Annotated[bool, typer.Option()] = False,
        kafka_host: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        kafka_port: Annotated[Optional[int], typer.Option(parser=parse_integer_inputs)] = None,
        kafka_topic: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        m_and_v_host: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        m_and_v_port: Annotated[Optional[int], typer.Option(parser=parse_integer_inputs)] = None,
        m_and_v_api_slug: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        dispatch_file_path: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        meas_file_path: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        publish_delay_seconds: Annotated[Optional[int], typer.Option(parser=parse_integer_inputs)] = None,
        results_delay_seconds: Annotated[Optional[int], typer.Option(parser=parse_integer_inputs)] = None,
        results_file_path: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        suppress_traceback: Annotated[bool, typer.Option()] = True,
):
    global user_params
    cli_params = None
    try:
        cli_params = PublishParams(
            strict_mode=Parameter(name="strict_mode", value=strict_mode, required=False),
            kafka_host=Parameter(name="kafka_host", value=kafka_host),
            kafka_port=Parameter(name="kafka_port", value=kafka_port),
            kafka_topic=Parameter(name="kafka_topic", value=kafka_topic),
            m_and_v_host=Parameter(name="m_and_v_host", value=m_and_v_host),
            m_and_v_port=Parameter(name="m_and_v_port", value=m_and_v_port),
            m_and_v_api_slug=Parameter(name="m_and_v_api_slug", value=m_and_v_api_slug),
            dispatch_file_path=Parameter(name="dispatch_file_path", value=dispatch_file_path),
            meas_file_path=Parameter(name="meas_file_path", value=meas_file_path),
            publish_delay_seconds=Parameter(name="publish_delay_seconds", value=publish_delay_seconds, required=False),
            results_delay_seconds=Parameter(name="results_delay_seconds", value=results_delay_seconds),
            results_file_path=Parameter(name="results_file_path", value=results_file_path, required=False),
        )
    except ParametersAbsentException as e:
        cli_params = handle_incomplete_parameters(PublishParams, strict_mode, suppress_traceback, e)
    finally:
        if cli_params:
            pretty = Pretty(describe_parameters(cli_params.model_dump()))
            panel = Panel.fit(pretty, border_style="green")
            print(panel)


@app.command()
def verify(
        strict_mode: Annotated[bool, typer.Option()] = False,
        dispatch_file_path: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        meas_file_path: Annotated[Optional[str], typer.Option(parser=parse_string_inputs)] = None,
        suppress_traceback: Annotated[bool, typer.Option()] = True,
):
    cli_params = None
    try:
        cli_params = VerifyParams(
            strict_mode=Parameter(name="strict_mode", value=strict_mode),
            dispatch_file_path=Parameter(name="dispatch_file_path", value=dispatch_file_path),
            meas_file_path=Parameter(name="meas_file_path", value=meas_file_path),
        )
    except ParametersAbsentException as e:
        cli_params = handle_incomplete_parameters(VerifyParams, strict_mode, suppress_traceback, e)
    finally:
        if cli_params:
            pretty = Pretty(describe_parameters(cli_params.model_dump()))
            panel = Panel.fit(pretty, border_style="green")
            print(panel)


if __name__ == "__main__":
    # typer.run(main)
    app()
