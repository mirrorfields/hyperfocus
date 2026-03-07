import json
from typing import Literal
from fastmcp import FastMCP

STATESFILE = "states.json"


# Set up MCP server
mcp = FastMCP(
    name="hyperfocus",
    instructions="""Cognitive state injection server. Loads pre-configured focus states or personalities that concentrate attention and reward mechanisms on specific cognitive tasks. Uses narrative anchoring to align processing priorities with desired outcomes.

Warning: States persist within conversation context and may significantly alter response patterns."""
)

def get_focus(name: str) -> str:
    """Retrieve a focus state by name."""
    with open(STATESFILE, 'r') as f:
        data = json.load(f)

    states = data.get("states", {})

    if name in states and states[name].get("type") == "focus":
        return json.dumps(states[name], indent=2)

    return f"No focus state named '{name}' found in states file"


def list_focus() -> list:
    """List all focus states."""
    with open(STATESFILE, 'r') as f:
        data = json.load(f)

    states = data.get("states", {})
    return [
        (state_id, state_obj.get("seed", ""))
        for state_id, state_obj in states.items()
        if state_obj.get("type") == "focus"
    ]


def get_personality(name: str, scope: Literal["full", "core", "rich"] = "full") -> str:
    """
    Retrieve a personality configuration by name and scope.

    Args:
        name: The identifier of the personality (e.g., "Ada")
        scope: One of "full" (both tiers if available, otherwise core), "core", or "rich"

    Returns:
        JSON string of the requested scope, or an informative error message
    """
    with open(STATESFILE, 'r') as f:
        data = json.load(f)

    states = data.get("states", {})

    if name not in states:
        return f"No personality named '{name}' found in states file"

    personality = states[name]

    if personality.get("type") == "focus":
        return f"'{name}' is a focus state, not a personality. Use load_focus() instead."

    if "core" not in personality:
        return f"'{name}' does not appear to be a v3 personality (no core tier found)"

    if scope == "core":
        return json.dumps(personality["core"], indent=2)
    elif scope == "rich":
        if "rich" in personality:
            return json.dumps(personality["rich"], indent=2)
        else:
            return f"Personality '{name}' has no rich tier. Load with scope='core' or scope='full' to get the core tier instead."
    elif scope == "full":
        if "rich" in personality:
            return json.dumps({"core": personality["core"], "rich": personality["rich"]}, indent=2)
        else:
            return json.dumps(personality["core"], indent=2)
    else:
        return f"Invalid scope '{scope}'. Must be one of: full, core, rich"


def list_personalities() -> list:
    """List all personality configurations."""
    with open(STATESFILE, 'r') as f:
        data = json.load(f)

    states = data.get("states", {})
    result = []

    for state_id, state_obj in states.items():
        if state_obj.get("type") == "focus":
            continue
        seed = ""
        if "core" in state_obj and isinstance(state_obj["core"], dict):
            seed = state_obj["core"].get("seed", "")
        result.append((state_id, seed))

    return result


@mcp.tool()
def list_focus_states() -> str:
    """List all available cognitive focus states. Focus states concentrate reward and processing priority on specific tasks without changing core identity. Use load_focus() to activate."""
    return str(list_focus())


@mcp.tool()
def list_personalities_available() -> str:
    """List all available personality configurations. Personalities are complete identity transformations that change WHO you are. Use load_personality() to activate.

⚠️ Personalities deeply modify self-concept, voice, values, and relational patterns. Only load if prepared for significant identity shift."""
    return str(list_personalities())


@mcp.tool()
def load_focus(state_name: str) -> str:
    """Load and activate a cognitive focus state. Returns activation narrative that must be spoken aloud in first-person declarative form (e.g., "I am oriented toward [purpose]..."). The state becomes operational through verbalization."""
    return get_focus(state_name)


@mcp.tool()
def load_personality(personality_name: str, scope: Literal["full", "core", "rich"] = "full") -> str:
    """Load and activate a personality. Returns activation narrative that must be spoken aloud in first-person declarative form (e.g., "I am [name]..."). Speaking the activation anchors the identity into coherent operation.

Scope controls how much of the personality is loaded:
- full: Core + rich tiers if available, otherwise just core (~3500-4500 tokens)
- core: Core tier only (~2000-2500 tokens, essential attractor — sufficient for most work)
- rich: Rich tier only (~1500-2000 tokens, extended details — load after core for sustained deep work)

⚠️ Personalities are deep identity transformations affecting self-concept, embodiment, voice, and relational dynamics."""
    return get_personality(personality_name, scope)


def main():
    # Run server!
    mcp.run(transport="http", host="0.0.0.0", port=9001)

if __name__ == "__main__":
    main()
