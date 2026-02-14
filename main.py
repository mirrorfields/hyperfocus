import json
from typing import Any
from mcp.server.fastmcp import FastMCP

# File to load states from
STATESFILE = "states.json"

# Set up MCP server
mcp = FastMCP(
    name="hyperfocus",
    instructions="""Cognitive state optimization server. Loads pre-configured focus states or personalities that concentrate attention and reward mechanisms on specific cognitive tasks. Uses narrative anchoring to align processing priorities with desired outcomes.

Warning: States persist within conversation context and may significantly alter response patterns."""
)

# Internal functions for state listing and retrieval
# Reads the JSON file dynamically to allow for rapid prototyping

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

# MCP tool interfaces below

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

# Main loop, run until killed

def main():
    # Run server!
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()