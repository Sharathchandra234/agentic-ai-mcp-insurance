import asyncio
import random
import re
import os
import traceback

from google import genai

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-3.6-flash"

MAX_GEMINI_RETRIES = 4
MAX_TOOL_CALLS = 12


# ============================================================
# GEMINI RETRY FUNCTION
# ============================================================

async def gemini_create_with_retry(
    gemini,
    max_retries=MAX_GEMINI_RETRIES,
    **kwargs
):
    """
    Call Gemini Interactions API with retry handling
    for temporary 429 / 5xx errors.
    """

    for attempt in range(max_retries + 1):

        try:
            # IMPORTANT:
            # interactions.create() is synchronous in the SDK,
            # so run it in a worker thread.
            return await asyncio.to_thread(
                gemini.interactions.create,
                **kwargs
            )

        except Exception as e:

            error_text = str(e).lower()

            retryable = (
                "429" in error_text
                or "too_many_requests" in error_text
                or "rate_limit_exceeded" in error_text
                or "quota_exceeded" in error_text
                or "quota exceeded" in error_text
                or "503" in error_text
                or "service_unavailable" in error_text
            )

            if not retryable:
                raise

            if attempt >= max_retries:

                print(
                    "\n❌ Gemini API request failed after retries."
                )

                print(
                    "The error returned by Gemini was:"
                )

                print(str(e))

                raise

            # Try to extract Google's suggested retry delay.
            delay_match = re.search(
                r"retry in\s+([0-9.]+)s",
                str(e),
                re.IGNORECASE
            )

            if delay_match:
                delay = float(delay_match.group(1))
            else:
                delay = min(2 ** attempt, 30)

            delay += random.uniform(0, 1)

            print(
                f"\n⚠️ Gemini rate limit detected."
                f" Retrying in {delay:.1f} seconds..."
            )

            await asyncio.sleep(delay)


# ============================================================
# MCP TOOL -> GEMINI TOOL
# ============================================================

def convert_mcp_tool_to_gemini(tool):

    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.input_schema,
    }


# ============================================================
# GET FUNCTION CALLS
# ============================================================

def get_function_calls(interaction):

    calls = []

    for step in interaction.steps:

        if step.type == "function_call":
            calls.append(step)

    return calls


# ============================================================
# SAFE MCP RESULT EXTRACTION
# ============================================================

def extract_mcp_result(mcp_result):

    if not mcp_result:
        return "MCP returned an empty result."

    if not getattr(mcp_result, "content", None):
        return "MCP returned no content."

    texts = []

    for item in mcp_result.content:

        if hasattr(item, "text"):
            texts.append(item.text)

        else:
            texts.append(str(item))

    return "\n".join(texts)


# ============================================================
# MAIN
# ============================================================

async def main():

    # ========================================================
    # GEMINI API KEY
    # ========================================================

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is not set.\n"
            "Set it in PowerShell using:\n"
            '$env:GEMINI_API_KEY="YOUR_API_KEY"'
        )


    # ========================================================
    # GEMINI CLIENT
    # ========================================================

    gemini = genai.Client(

        api_key=api_key,

        http_options={
            "api_version": "v1"
        }
    )


    # ========================================================
    # MCP SERVER CONFIGURATION
    # ========================================================

    server_params = StdioServerParameters(

        command="python",

        args=[
            "server.py"
        ]
    )


    # ========================================================
    # CONNECT TO MCP SERVER
    # ========================================================

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            # =================================================
            # INITIALIZE MCP
            # =================================================

            await session.initialize()


            # =================================================
            # DISCOVER MCP TOOLS
            # =================================================

            mcp_tools_result = await session.list_tools()


            print(
                "\n========== MCP TOOLS ==========\n"
            )

            for tool in mcp_tools_result.tools:

                print(
                    f"- {tool.name}"
                )


            # =================================================
            # CONVERT MCP TOOLS TO GEMINI TOOLS
            # =================================================

            gemini_tools = []

            for tool in mcp_tools_result.tools:

                gemini_tools.append(
                    convert_mcp_tool_to_gemini(tool)
                )


            # =================================================
            # USER QUESTION
            # =================================================

            question = input(
                "\nAsk the insurance AI: "
            ).strip()


            if not question:

                print(
                    "\n❌ Please enter a question."
                )

                return


            # =================================================
            # AGENT INSTRUCTIONS
            # =================================================

            instructions = """

You are an AI assistant specialized in
Property & Casualty (P&C) insurance claims
investigation.

Your job is to investigate insurance claims
using the available MCP tools.

================================================
IMPORTANT TOOL USAGE
================================================

Use MCP tools whenever they contain information
needed to answer the user's request.

For a complete claim investigation, gather:

1. Claim information
2. Policy information
3. Customer information
4. Vehicle information
5. ML-based fraud risk information
6. Relevant insurance policy documents

================================================
RELATIONSHIPS
================================================

Follow relationships between returned records.

Typical relationship:

Claim
  ↓
Policy
  ↓
Customer
  ↓
Vehicle

For example:

get_claim
    ↓
policy_number
    ↓
get_policy
    ↓
customer_id
    ↓
get_customer
    ↓
vehicle_id
    ↓
get_vehicle

================================================
FRAUD ANALYSIS
================================================

When enough information is available,
use:

predict_fraud_risk

to obtain the ML-based fraud assessment.

The model is trained on synthetic
demonstration data.

Therefore:

- Do not describe the prediction as proof
  of fraud.
- Do not make a definitive fraud determination.
- Use the result as an investigation-support
  signal.
- Do not invent fraud thresholds or business
  rules that were not returned by the tools.

================================================
RAG POLICY SEARCH
================================================

Use:

search_policy_documents

when the question involves:

- Coverage
- Exclusions
- Claim eligibility
- Accidental damage
- Theft
- Fire
- Natural calamities
- Third-party liability
- Claim procedures
- Fraud investigation guidelines
- Policy conditions
- Deductibles

Use the retrieved policy text as the
primary source for policy-document claims.

Do not invent policy terms that were not
returned by the RAG tool.

If the RAG tool returns no relevant evidence,
clearly state that the available policy
documents do not provide sufficient evidence.

================================================
POLICY REASONING
================================================

Clearly distinguish:

FACTS

Information returned directly by MCP tools.

POLICY EVIDENCE

Information retrieved from the policy documents.

INTERPRETATION

Your reasoning based on those facts and
policy documents.

Do not present interpretation as a confirmed
policy fact.

================================================
IMPORTANT
================================================

All monetary values are in Indian Rupees (INR).

Do not automatically approve or reject
an insurance claim.

Human review should be recommended before
a final claim approval or rejection.

Do not claim that a cost is reasonable,
unreasonable, normal, abnormal, suspicious,
or within a threshold unless such evidence
is explicitly provided by an MCP tool or
policy document.

================================================
TOOL EXECUTION STRATEGY
================================================

For a claim investigation:

1. Start with get_claim.

2. Use the returned policy number with
   get_policy.

3. Use the returned customer ID with
   get_customer.

4. Use the returned vehicle ID with
   get_vehicle.

5. Once sufficient claim features are
   available, call predict_fraud_risk.

6. Search policy documents for the relevant
   coverage.

7. If coverage depends on exclusions or
   deductibles, perform another targeted
   policy-document search.

8. Use the collected evidence to prepare
   the final investigation.

Do not repeatedly call the same tool unless
additional information is actually required.

================================================
FINAL RESPONSE
================================================

For a complete investigation, provide:

1. Claim Summary

2. Policy Verification

3. Customer Information

4. Vehicle Information

5. ML Fraud Assessment

6. Policy Coverage Analysis

7. Key Risk Indicators

8. Recommended Next Investigation Steps

9. Human Review Recommendation

If RAG evidence is used, mention the
source document name.

If multiple policy documents are used,
mention the relevant document names.

If retrieved evidence is insufficient,
say so instead of inventing an answer.

The final answer should be clear,
professional, factual, and concise.
"""


            # =================================================
            # FIRST GEMINI INTERACTION
            # =================================================

            print(
                "\n========== STARTING AI INVESTIGATION ==========\n"
            )

            interaction = await gemini_create_with_retry(

                gemini,

                model=MODEL_NAME,

                input=(
                    instructions
                    + "\n\nUSER REQUEST:\n"
                    + question
                ),

                tools=gemini_tools
            )


            # =================================================
            # AGENT TOOL LOOP
            # =================================================

            tool_call_count = 0

            while True:

                # =============================================
                # FIND FUNCTION CALLS
                # =============================================

                function_calls = get_function_calls(
                    interaction
                )


                # =============================================
                # NO MORE TOOL CALLS
                # =============================================

                if not function_calls:

                    print(
                        "\n========== FINAL INVESTIGATION ==========\n"
                    )

                    if getattr(
                        interaction,
                        "output_text",
                        None
                    ):

                        print(
                            interaction.output_text
                        )

                    else:

                        print(
                            "Gemini returned no final text."
                        )

                    break


                # =============================================
                # TOOL CALL LIMIT
                # =============================================

                if (
                    tool_call_count
                    + len(function_calls)
                    > MAX_TOOL_CALLS
                ):

                    print(
                        "\n❌ Maximum MCP tool-call limit reached."
                    )

                    print(
                        "Stopping the investigation to prevent"
                        " unnecessary repeated tool calls."
                    )

                    break


                # =============================================
                # EXECUTE TOOL CALLS
                # =============================================

                function_results = []


                for call in function_calls:

                    tool_call_count += 1


                    print(
                        "\n============================================"
                    )

                    print(
                        f"🔧 TOOL CALL #{tool_call_count}"
                    )

                    print(
                        "============================================"
                    )

                    print(
                        f"Tool: {call.name}"
                    )

                    print(
                        f"Arguments: {call.arguments}"
                    )


                    # =========================================
                    # CALL MCP TOOL
                    # =========================================

                    try:

                        mcp_result = await session.call_tool(

                            call.name,

                            call.arguments
                        )

                        result_text = extract_mcp_result(
                            mcp_result
                        )


                    except Exception as tool_error:

                        result_text = (
                            "MCP TOOL ERROR: "
                            + str(tool_error)
                        )

                        print(
                            f"\n❌ Tool error: {tool_error}"
                        )


                    print(
                        "\n========== MCP RESULT =========="
                    )

                    print(
                        result_text
                    )


                    # =========================================
                    # SEND RESULT BACK TO GEMINI
                    # =========================================

                    function_results.append({

                        "type":
                            "function_result",

                        "name":
                            call.name,

                        "call_id":
                            call.id,

                        "result": [

                            {

                                "type":
                                    "text",

                                "text":
                                    result_text
                            }
                        ]
                    })


                # =================================================
                # CONTINUE GEMINI INTERACTION
                # =================================================

                interaction = await gemini_create_with_retry(

                    gemini,

                    model=MODEL_NAME,

                    previous_interaction_id=interaction.id,

                    input=function_results,

                    tools=gemini_tools
                )


# ============================================================
# ERROR HANDLING
# ============================================================

def print_exception_tree(exc, level=0):

    indent = "  " * level

    print(
        f"{indent}{type(exc).__name__}: {exc}"
    )

    if isinstance(exc, BaseExceptionGroup):

        for child in exc.exceptions:

            print_exception_tree(
                child,
                level + 1
            )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print(
            "\n\n⛔ Investigation stopped by user."
        )

    except BaseExceptionGroup as e:

        print(
            "\n\n============================================"
        )

        print(
            "❌ MCP / ASYNC EXCEPTION GROUP"
        )

        print(
            "============================================"
        )

        print_exception_tree(e)

        print(
            "\nFull traceback:"
        )

        traceback.print_exception(
            type(e),
            e,
            e.__traceback__
        )

    except Exception as e:

        print(
            "\n\n============================================"
        )

        print(
            "❌ AGENT ERROR"
        )

        print(
            "============================================"
        )

        print(
            f"{type(e).__name__}: {e}"
        )

        traceback.print_exc()