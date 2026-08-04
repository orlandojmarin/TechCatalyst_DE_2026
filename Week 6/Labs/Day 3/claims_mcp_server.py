"""A tiny MCP server exposing the claim tools from Activity 4."""

from mcp.server import MCPServer

mcp = MCPServer("claims-tools")

CLAIMS_DB = {
    "CLM_101": {"status": "Approved", "amount": 3400.0, "type": "Auto Collision"},
    "CLM_102": {"status": "Approved", "amount": 1250.0, "type": "Property Loss"},
    "CLM_103": {"status": "Denied", "amount": 0.0, "type": "Fraud Flag"},
}

POLICIES_DB = {
    "POL_991": {"deductible": 500.0, "coverage": "Full Comprehensive"},
    "POL_992": {"deductible": 1000.0, "coverage": "Liability Only"},
}


@mcp.tool()
def get_claim_status(claim_id: str) -> dict:
    """Look up an insurance claim's status, amount, and type by claim ID."""
    return CLAIMS_DB.get(claim_id, {"error": f"{claim_id} not found"})


@mcp.tool()
def get_policy_deductible(policy_id: str) -> dict:
    """Look up a policy's deductible amount and coverage type by policy ID."""
    return POLICIES_DB.get(policy_id, {"error": f"{policy_id} not found"})


@mcp.tool()
def calculate_net_payout(claim_amount: float, deductible: float) -> dict:
    """Subtract a deductible from a claim amount to get the net payout."""
    return {"net_payout": round(max(0.0, claim_amount - deductible), 2)}


if __name__ == "__main__":
    mcp.run()
