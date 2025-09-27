from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(location: str) -> str:
    """Provides the weather for the given city"""
    return "Hot as hell"

if __name__=="__main__":
    mcp.run(transport="sse")