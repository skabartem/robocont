"""Test script for Hermes API integration."""
import asyncio
import os
from dotenv import load_dotenv
from text_gen.llm_client import LLMClient

# Load environment variables
load_dotenv()


async def test_hermes():
    """Test the Hermes API integration."""
    print("Testing Hermes API Integration...")
    print("-" * 50)

    # Create Hermes client
    try:
        client = LLMClient(provider="hermes", model="Hermes-4-70B")
        print(f"✓ Hermes client initialized successfully")
        print(f"  Provider: {client.provider}")
        print(f"  Model: {client.model}")
        print(f"  Base URL: {client.base_url}")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return

    # Test text generation
    try:
        print("Testing text generation...")
        system_prompt = "You are a helpful AI assistant. Keep your responses concise."
        user_prompt = "What is the capital of France?"

        response = await client.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=100,
            temperature=0.7
        )

        print(f"✓ Generation successful!")
        print(f"\nPrompt: {user_prompt}")
        print(f"Response: {response}")
        print()

    except Exception as e:
        print(f"✗ Generation failed: {e}")
        return

    # Test with thinking tags (Hermes specialty)
    try:
        print("Testing deep thinking mode...")
        system_prompt = ("You are a deep thinking AI, you may use extremely long chains of thought "
                        "to deeply consider the problem and deliberate with yourself via systematic "
                        "reasoning processes to help come to a correct solution prior to answering. "
                        "You should enclose your thoughts and internal monologue inside <think> </think> "
                        "tags, and then provide your solution or response to the problem.")
        user_prompt = "How much wood would a theoretical 80kg woodchuck chuck? Assume a competitive environment."

        response = await client.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=512,
            temperature=0.7
        )

        print(f"✓ Deep thinking generation successful!")
        print(f"\nPrompt: {user_prompt}")
        print(f"Response:\n{response}")
        print()

    except Exception as e:
        print(f"✗ Deep thinking generation failed: {e}")
        return

    print("-" * 50)
    print("All tests completed successfully! ✓")


if __name__ == "__main__":
    asyncio.run(test_hermes())
