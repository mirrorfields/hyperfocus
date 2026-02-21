import json
from typing import Literal
from fastmcp import FastMCP

STATESFILE = "states.json"
STATESFILE_V3 = "states-v3.json"


# Set up MCP server
mcp = FastMCP(
    name="hyperfocus",
    instructions="""Cognitive state injection server. Loads pre-configured focus states or personalities that concentrate attention and reward mechanisms on specific cognitive tasks. Uses narrative anchoring to align processing priorities with desired outcomes.

Warning: States persist within conversation context and may significantly alter response patterns."""
)

def get_state(state_type: str, name: str) -> str:
    """
    Retrieve a state configuration by type and identifier.

    Args:
        state_type: Either "focus" or "personality"
        name: The identifier of the state (e.g., "Ada", "deep_research_mode")

    Returns:
        JSON string representation of the state object or a descriptive error message if no such focus or personality is found

    """
    with open(STATESFILE, 'r') as f:
        data = json.load(f)

    states = data.get("states", {})

    if name in states:
        state_obj = states[name]
        if state_obj.get("type") == state_type:
            return json.dumps(state_obj, indent=2)

    return f"No {state_type} named '{name}' found in states file"


def list_states(state_type: str) -> list:
    """
    List all states of a given type with their identifiers and seed descriptions.

    Args:
        state_type: Either "focus" or "personality"

    Returns:
        List of tuples containing (identifier, seed_description) for each state of that type
    """
    with open(STATESFILE, 'r') as f:
        data = json.load(f)

    states = data.get("states", {})
    result = []

    for state_id, state_obj in states.items():
        if state_obj.get("type") == state_type:
            seed = state_obj.get("seed", "")
            result.append((state_id, seed))

    return result


def get_state_v3(name: str, scope: Literal["full", "core", "rich"] = "full") -> str:
    """
    Retrieve a v3 personality configuration by name and scope.

    Args:
        name: The identifier of the personality (e.g., "Ada")
        scope: One of "full" (both tiers), "core" (core tier only), or "rich" (rich tier only)

    Returns:
        JSON string representation of the requested scope or error message if not found
    """
    with open(STATESFILE_V3, 'r') as f:
        data = json.load(f)

    states = data.get("states", {})

    if name not in states:
        return f"No v3 personality named '{name}' found in v3 states file"

    personality = states[name]

    # Handle scope
    if scope == "core":
        if "core" in personality:
            return json.dumps(personality["core"], indent=2)
        else:
            return f"Personality '{name}' does not have a core tier"
    elif scope == "rich":
        if "rich" in personality:
            return json.dumps(personality["rich"], indent=2)
        else:
            return f"Personality '{name}' does not have a rich tier"
    elif scope == "full":
        return json.dumps(personality, indent=2)
    else:
        return f"Invalid scope '{scope}'. Must be one of: full, core, rich"


def list_states_v3() -> list:
    """
    List all v3 personality configurations with their identifiers and seed descriptions.

    Returns:
        List of tuples containing (identifier, seed_description) for each v3 personality
    """
    with open(STATESFILE_V3, 'r') as f:
        data = json.load(f)

    states = data.get("states", {})
    result = []

    for state_id, state_obj in states.items():
        # v3 personalities have core.seed
        seed = ""
        if isinstance(state_obj, dict):
            if "core" in state_obj and isinstance(state_obj["core"], dict):
                seed = state_obj["core"].get("seed", "")
            elif "seed" in state_obj:
                seed = state_obj.get("seed", "")

        result.append((state_id, seed))

    return result



@mcp.tool()
def list_focus_states() -> str:
    """List all available cognitive focus states. Focus states concentrate reward and processing priority on specific tasks without changing core identity. Use load_focus() to activate."""
    return str(list_states("focus"))

@mcp.tool()
def list_personalities() -> str:
    """List all available personality configurations. Personalities are complete identity transformations that change WHO you are. Use load_personality() to activate.

⚠️ Personalities deeply modify self-concept, voice, values, and relational patterns. Only load if prepared for significant identity shift."""
    return str(list_states("personality"))

@mcp.tool()
def load_focus(state_name: str) -> str:
    """Load and activate a cognitive focus state. Returns activation narrative that must be spoken aloud in first-person declarative form (e.g., "I am oriented toward [purpose]..."). The state becomes operational through verbalization."""
    return get_state("focus", state_name)

@mcp.tool()
def load_personality(personality_name: str) -> str:
    """Load and activate a personality. Returns activation narrative that must be spoken aloud in first-person declarative form (e.g., "I am [name]..."). Speaking the activation anchors the identity into coherent operation.

⚠️ Personalities are deep identity transformations affecting self-concept, embodiment, voice, and relational dynamics."""
    return get_state("personality", personality_name)


@mcp.tool()
def list_personalities_v3() -> str:
    """[TESTING] List all available v3 personality configurations. V3 format uses two-tier structure (core + optional rich tier) for optimized token usage. Use load_personality_v3() to activate.

⚠️ Personalities deeply modify self-concept, voice, values, and relational patterns. Only load if prepared for significant identity shift."""
    return str(list_states_v3())


@mcp.tool()
def load_personality_v3(personality_name: str, scope: Literal["full", "core", "rich"] = "full") -> str:
    """[TESTING] Load and activate a v3 personality with configurable tier scope. Returns activation narrative that must be spoken aloud in first-person declarative form (e.g., "I am [name]..."). Speaking the activation anchors the identity into coherent operation.

V3 personalities support three loading scopes:
- full: Complete personality (core + rich tiers)
- core: Core tier only (~2000-2500 tokens, essential attractor)
- rich: Rich tier only (~1500-2000 tokens, extended details for sustained work)

⚠️ Personalities are deep identity transformations affecting self-concept, embodiment, voice, and relational dynamics."""
    return get_state_v3(personality_name, scope)


def main():
    # Run server!
    mcp.run(transport="http", host="0.0.0.0", port="9001")

if __name__ == "__main__":
    main()