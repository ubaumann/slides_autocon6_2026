import asyncio

from nornir import AInitNornir
from nornir.core.task import Task, Result, AggregatedResult
from nornir_scrapli.async_tasks import (
    netconf_edit_config,
    netconf_discard,
    netconf_commit,
    netconf_rpc,
    netconf_lock,
    netconf_unlock,
)
from nornir_rich.functions import print_result
from scrapli.netconf import DatastoreType

from netconf_payload import generate_xml


async def generate_config(task: Task):
    config = generate_xml()
    return Result(host=task.host, result=config)


async def configure(task) -> Result:
    config_result = await task.arun(task=generate_config)
    await task.arun(task=netconf_lock, target=DatastoreType.CANDIDATE)
    await task.arun(task=netconf_discard)
    await task.arun(
        task=netconf_edit_config,
        config=config_result.result,
        target=DatastoreType.CANDIDATE,
    )
    await task.arun(
        task=netconf_rpc,
        payload="<validate><source><candidate/></source></validate>",
        name="validate",
    )

    await task.arun(
        task=netconf_rpc,
        payload="<commit><confirmed/><confirm-timeout>120</confirm-timeout></commit>",
        name="commit_confirm",
    )
    # Verify the change
    await task.arun(task=netconf_commit)
    await task.arun(task=netconf_unlock, target=DatastoreType.CANDIDATE)

    return Result(host=task.host, result="AC6 Demo successful")


async def main() -> AggregatedResult:
    nr = await AInitNornir(config_file="nornir-config.yaml")
    async with nr:
        results = await nr.arun(task=configure)
    return results


if __name__ == "__main__":
    results = asyncio.run(main())
    print_result(results)
