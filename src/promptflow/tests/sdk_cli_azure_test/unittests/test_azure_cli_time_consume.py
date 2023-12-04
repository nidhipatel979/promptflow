import contextlib
import multiprocessing
import sys
import timeit
from unittest import mock
import pytest
from promptflow._core.operation_context import OperationContext
from promptflow._cli._user_agent import USER_AGENT as CLI_USER_AGENT  # noqa: E402

FLOWS_DIR = "./tests/test_configs/flows"
DATAS_DIR = "./tests/test_configs/datas"


@contextlib.contextmanager
def check_ua():
    cli_perf_monitor_agent = "perf_monitor/1.0"
    default_context = OperationContext.get_instance()
    try:
        instance = OperationContext()
        OperationContext._current_context.set(instance)

        context = OperationContext.get_instance()
        context.append_user_agent(cli_perf_monitor_agent)
        assert cli_perf_monitor_agent in context.get_user_agent()
        yield
        assert CLI_USER_AGENT in context.get_user_agent()
    except Exception as e:
        raise e
    finally:
        OperationContext._current_context.set(default_context)
        context = OperationContext.get_instance()
        assert cli_perf_monitor_agent not in context.get_user_agent()


def run_cli_command(cmd, time_limit=3600):
    from promptflow._cli._pf_azure.entry import main
    from promptflow.azure.operations._run_operations import RunOperations

    with mock.patch.object(RunOperations, "create_or_update") as create_or_update_fun, mock.patch.object(
        RunOperations, "update"
    ) as update_fun, mock.patch.object(RunOperations, "get") as get_fun, mock.patch.object(
        RunOperations, "restore"
    ) as restore_fun:
        create_or_update_fun.return_value._to_dict.return_value = {"name": "test_run"}
        update_fun.return_value._to_dict.return_value = {"name": "test_run"}
        get_fun.return_value._to_dict.return_value = {"name": "test_run"}
        restore_fun.return_value._to_dict.return_value = {"name": "test_run"}

        sys.argv = list(cmd)
        st = timeit.default_timer()
        with check_ua():
            main()
        ed = timeit.default_timer()

        print(f"{cmd}, \nTotal time: {ed - st}s")
        context = OperationContext.get_instance()
        print("request id: ", context.get("request_id"))
        assert ed - st < time_limit, f"The time limit is {time_limit}s, but it took {ed - st}s."


def subprocess_run_cli_command(cmd, time_limit=3600):
    process = multiprocessing.Process(target=run_cli_command, args=(cmd,), kwargs={"time_limit": time_limit})
    process.start()
    process.join()
    assert process.exitcode == 0


@pytest.fixture
def operation_scope_args(subscription_id: str, resource_group_name: str, workspace_name: str):
    return [
        "--subscription",
        subscription_id,
        "--resource-group",
        resource_group_name,
        "--workspace-name",
        workspace_name,
    ]


@pytest.mark.usefixtures("mock_get_azure_pf_client")
@pytest.mark.unittest
class TestAzureCliTimeConsume:
    def test_pfazure_run_create(self, operation_scope_args, time_limit=30):
        run_cli_command(
            cmd=(
                "pfazure",
                "run",
                "create",
                "--flow",
                f"{FLOWS_DIR}/print_input_flow",
                "--data",
                f"{DATAS_DIR}/print_input_flow.jsonl",
                *operation_scope_args,
            ),
            time_limit=time_limit,
        )

    def test_pfazure_run_update(self, operation_scope_args, time_limit=30):
        run_cli_command(
            cmd=(
                "pfazure",
                "run",
                "update",
                "--name",
                "test_run",
                "--set",
                "display_name=test_run",
                "description='test_description'",
                "tags.key1=value1",
                *operation_scope_args,
            ),
            time_limit=time_limit,
        )

    def test_run_restore(self, operation_scope_args, time_limit=30):
        run_cli_command(
            cmd=(
                "pfazure",
                "run",
                "restore",
                "--name",
                "test_run",
                *operation_scope_args,
            ),
            time_limit=time_limit,
        )
