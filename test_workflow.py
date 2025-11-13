import pytest
from temporal_agent import get_time_activity, list_files_activity
from client import generate_workflow_id


@pytest.mark.asyncio
async def test_get_time_activity():
    result = await get_time_activity()
    assert len(result) == 19  # YYYY-MM-DD HH:MM:SS format
    assert "-" in result and ":" in result


@pytest.mark.asyncio
async def test_list_files_activity():
    result = await list_files_activity()
    assert "Files:" in result
    assert ".py" in result


def test_workflow_id_uniqueness():
    wf_id1 = generate_workflow_id("test task")
    wf_id2 = generate_workflow_id("test task")
    assert wf_id1 != wf_id2  # UUIDs should be different


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
