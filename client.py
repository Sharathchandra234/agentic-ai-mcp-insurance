import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # Ask the user for the claim ID
    claim_id = input("Enter Claim ID: ")

    # Configuration for starting the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):

        # Create an MCP client session
        async with ClientSession(read, write) as session:

            # Initialize the MCP connection
            await session.initialize()

            # --------------------------------------------------
            # Step 1: Get Claim
            # --------------------------------------------------

            claim_result = await session.call_tool(
                "get_claim",
                {"claim_id": claim_id}
            )

            claim_data = json.loads(
                claim_result.content[0].text
            )

            print("\n========== CLAIM INFORMATION ==========")
            print(json.dumps(claim_data, indent=2))

            # Check whether claim exists
            if "error" in claim_data:
                print("\nClaim not found.")
                return

            # --------------------------------------------------
            # Step 2: Get Policy
            # --------------------------------------------------

            policy_number = claim_data["policy_number"]

            policy_result = await session.call_tool(
                "get_policy",
                {"policy_number": policy_number}
            )

            policy_data = json.loads(
                policy_result.content[0].text
            )

            print("\n========== POLICY INFORMATION ==========")
            print(json.dumps(policy_data, indent=2))

            # Check whether policy exists
            if "error" in policy_data:
                print("\nPolicy not found.")
                return

            # --------------------------------------------------
            # Step 3: Get Customer
            # --------------------------------------------------

            customer_id = policy_data["customer_id"]

            customer_result = await session.call_tool(
                "get_customer",
                {"customer_id": customer_id}
            )

            customer_data = json.loads(
                customer_result.content[0].text
            )

            print("\n========== CUSTOMER INFORMATION ==========")
            print(json.dumps(customer_data, indent=2))

            # Check whether customer exists
            if "error" in customer_data:
                print("\nCustomer not found.")
                return

            # --------------------------------------------------
            # Step 4: Calculate Fraud Score
            # --------------------------------------------------

            claim_amount = claim_data["claim_amount"]
            previous_claims = customer_data["previous_claims"]

            fraud_result = await session.call_tool(
                "calculate_fraud_score",
                {
                    "claim_amount": claim_amount,
                    "previous_claims": previous_claims
                }
            )

            fraud_data = json.loads(
                fraud_result.content[0].text
            )

            print("\n========== FRAUD ASSESSMENT ==========")
            print(json.dumps(fraud_data, indent=2))

            # --------------------------------------------------
            # Final Investigation Summary
            # --------------------------------------------------

            print("\n========== INVESTIGATION SUMMARY ==========")

            print(f"Claim ID: {claim_data['claim_id']}")
            print(f"Policy Number: {policy_data['policy_number']}")
            print(f"Customer ID: {customer_data['customer_id']}")
            print(f"Claim Amount: ₹{claim_amount}")
            print(f"Previous Claims: {previous_claims}")
            print(f"Fraud Score: {fraud_data['fraud_score']}")
            print(f"Risk Level: {fraud_data['risk_level']}")


if __name__ == "__main__":
    asyncio.run(main())