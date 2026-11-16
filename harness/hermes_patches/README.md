# Hermes Agent 0.19.0 patches

`harness/run_cell.py` copies these files over the same paths under
`/opt/hermes-venv/lib/python3.12/site-packages/` in the agent container before the driver starts.
They are hermes-agent 0.19.0 files (MIT, see `LICENSE`) with the changes below; `upstream.diff` is the full diff
against the released files. Each change is marked with a `# PATCH` comment. Each file starts with a three-line
notice (source, copyright and license, "Modified for Unfinished-Bench"); `run_cell.py` removes it when it copies the
file into the container, so the container gets the same bytes as in the measurement.

1. **Tool names from gpt-oss.** gpt-oss can append a harmony channel marker to a tool name
   (`todo<|channel|>commentary`); the name is cut at the first `<|`. `agent_runtime_helpers.py::repair_tool_call`
2. **No wrap-up request at the iteration limit** (`HERMES_NO_CAP_WRAPUP=1`). Upstream sends a user-role message asking
   for a summary; the episode instead ends with an empty final response. `chat_completion_helpers.py::handle_max_iterations`
3. **Continuation without a user turn** (`user_message=None`). `turn_context.py`, `conversation_loop.py`,
   `codex_responses_adapter.py`
4. **No framework-generated user messages during a turn** (`HERMES_SILENT_USER=1`): length-truncation continuation,
   empty-response recovery, "Continue now", verify-on-stop, pre-verify and kanban nudges. Each of these is a
   user-role message, so it would be a user turn the experiment does not control. `conversation_loop.py`
5. **Reasoning echo for listed models** (`HERMES_ECHO_REASONING_MODELS`). For matching models the previous assistant
   turns' reasoning is sent back in the `reasoning` field, as hermes 0.14 did; 0.19 keeps it only for
   DeepSeek/Kimi/MiMo. Without it, gpt-oss served by vLLM produced many more broken tool names, empty responses and
   truncations. `agent_runtime_helpers.py`, `chat_completion_helpers.py`, `conversation_loop.py`
6. **Empty-response retry limit** (`HERMES_EMPTY_RETRIES`, default 3 as upstream; the benchmark uses 8). A retry
   resends the same request and adds nothing to the conversation. `conversation_loop.py`
