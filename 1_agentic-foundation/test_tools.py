from types import SimpleNamespace

from career_twin.tools import handle_tool_calls

fake_call = SimpleNamespace(
    id="t1",
    function=SimpleNamespace(
        name="record_unknown_question",
        arguments='{"question": "module test question"}',
    ),
)

print(handle_tool_calls([fake_call]))