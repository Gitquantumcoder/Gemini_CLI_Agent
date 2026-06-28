import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

SUPPORTED_IMAGE_FORMATS = {
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png":  "image/png",
    ".webp": "image/webp",
    ".gif":  "image/gif",
    ".bmp":  "image/bmp",
    ".tiff": "image/tiff",
    ".tif":  "image/tiff",
    ".heic": "image/heic",
    ".heif": "image/heif",
}

IMAGE_GENERATION_TRIGGERS = [
    "generate an image",
    "create an image",
    "create a picture",
    "draw a picture",
    "make an image",
    "generate a picture",
    "display an image"
]

# ── Change 5: system prompt enforces concise, line-wrapped replies ──────────
CONCISENESS_SUFFIX = (
    "\n\nIMPORTANT RESPONSE RULES:\n"
    "- Be concise and to the point. No padding or filler.\n"
    "- Keep every line to 30-40 words maximum.\n"
    "- Wrap text to a new line after 30-40 words.\n"
    "- Avoid long blocks; prefer short, clear sentences.\n"
    "- Do NOT over-explain. Give only what is needed."
)


def read_image_bytes(image_path: str) -> bytes | None:
    try:
        with open(image_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"  ❌ File not found: '{image_path}'")
        return None


def get_mime_type(image_path: str) -> str | None:
    extension = os.path.splitext(image_path)[1].lower()
    return SUPPORTED_IMAGE_FORMATS.get(extension, None)


def wants_image_output(user_text: str) -> bool:
    lowered = user_text.lower()
    return any(trigger in lowered for trigger in IMAGE_GENERATION_TRIGGERS)


def add_to_memory(memory: list, role: str, text: str):
    memory.append({"role": role, "text": text})


def show_memory(memory: list):
    print("\n  📋 [Memory] Full conversation so far:")
    for i, msg in enumerate(memory):
        # Change 1 & 2: "Pikachu" label + pikachu emoji instead of "Bot 🤖"
        prefix = "  You     " if msg["role"] == "user" else "  Pikachu ⚡🐹"
        print(f"    [{i+1}] {prefix}: {msg['text'][:80]}...")
    print()


def handle_agent_turn(
    client: genai.Client,
    memory: list,
    user_text: str,
    image_path: str | None,
    system_prompt: str,
    temperature: float,
) -> str:

    add_to_memory(memory, "user", user_text)

    # Inject conciseness rules into every call
    effective_system = system_prompt + CONCISENESS_SUFFIX

    if wants_image_output(user_text):
        # Change 2: pikachu emoji instead of 🎨 agent label
        print("\n⚡🐹 [Pikachu] Image generation request → Imagen 3...")

        try:
            imagen_response = client.models.generate_images(
                model="gemini-2.5-flash-image",
                prompt=user_text,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                ),
            )

            for i, generated_img in enumerate(imagen_response.generated_images):
                output_filename = f"generated_image_{i + 1}.jpg"
                with open(output_filename, "wb") as f:
                    f.write(generated_img.image.image_bytes)
                print(f"  ✅ Saved image → '{output_filename}'")

            reply = "Image generated and saved as 'generated_image_1.jpg'."

        except Exception as e:
            reply = f"❌ Image generation failed: {e}"

        add_to_memory(memory, "assistant", reply)
        return reply

    elif image_path:
        # Change 2: pikachu emoji
        print(f"\n  ⚡🐹 [Pikachu] Analyzing image: '{image_path}'...")

        mime_type = get_mime_type(image_path)
        if mime_type is None:
            ext = os.path.splitext(image_path)[1]
            reply = (
                f"❌ Unsupported format '{ext}'. "
                f"Supported: {', '.join(SUPPORTED_IMAGE_FORMATS.keys())}"
            )
            add_to_memory(memory, "assistant", reply)
            return reply

        raw_bytes = read_image_bytes(image_path)
        if raw_bytes is None:
            reply = "❌ Could not read the image file. Check the path."
            add_to_memory(memory, "assistant", reply)
            return reply

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=raw_bytes, mime_type=mime_type),
                    user_text,
                ],
                config=types.GenerateContentConfig(
                    system_instruction=effective_system,
                    temperature=temperature,
                ),
            )
            reply = response.text

        except Exception as e:
            reply = f"❌ Image analysis failed: {e}"

        add_to_memory(memory, "assistant", reply)
        return reply

    else:
        # Change 2: pikachu emoji
        print("\n ⚡🐹 [Pikachu] Thinking...")

        conversation_parts = []
        for msg in memory:
            prefix = "User" if msg["role"] == "user" else "Assistant"
            conversation_parts.append(f"{prefix}: {msg['text']}")

        full_conversation = "\n".join(conversation_parts)

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=full_conversation,
                config=types.GenerateContentConfig(
                    system_instruction=effective_system,
                    temperature=temperature,
                ),
            )
            reply = response.text

        except Exception as e:
            reply = f"❌ Text generation failed: {e}"

        add_to_memory(memory, "assistant", reply)
        return reply


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="⚡🐹 Pikachu AI Agent — text & image I/O",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help=(
            "Controls creativity of text responses.\n"
            "  0.0 = deterministic / factual\n"
            "  1.0 = balanced (default: 0.7)\n"
            "  2.0 = highly creative / random\n"
        ),
    )
    parser.add_argument(
        "--system",
        type=str,
        default="You are a helpful, friendly AI assistant.add a new line character after 20 words",
        help="System prompt that sets the agent's personality and behavior.",
    )
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    if not api_key:
        print("❌ No API key found.")
        print("   Set it with: export GEMINI_API_KEY=your_key")
        return

    client = genai.Client(api_key=api_key)
    memory = []
    print("\n","-"*20)
    print("  ⚡🐹 Pikachu here <3")
    print(f"  Temperature : {args.temperature}  (0=factual, 2=creative)")
    print(f"  Personality : {args.system[:60]}...")
    print("=" * 60)
    print("\n  COMMANDS:")
    print("  - Type normally to chat.")
    print("  - Say 'generate an image of ...' to create images.")
    print("  - Attach an image file to analyze it.")
    print("  - Type 'history' to view chat memory.")
    print("  - Type 'clear' to reset memory.")
    print("  - Type 'exit' to quit.")
    print()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("\n ⚡🐹 Pika pika! Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "history":
            if not memory:
                print("  📋 Memory is empty.\n")
            else:
                show_memory(memory)
            continue

        if user_input.lower() == "clear":
            memory.clear()
            print("  🗑️  Memory cleared.\n")
            continue

        has_image = input("  Attach an image? (yes/no): ").strip().lower()
        attached_image = None

        if has_image in ("yes", "y"):
            path_input = input("  Image path: ").strip()
            attached_image = path_input.strip("'\"")

        reply = handle_agent_turn(
            client        = client,
            memory        = memory,
            user_text     = user_input,
            image_path    = attached_image,
            system_prompt = args.system,
            temperature   = args.temperature,
        )

        # Change 1 & 2: reply label is "Pikachu ⚡🐹" instead of "Agent 🤖"
        print(f"\n  Pikachu⚡🐹: {reply}\n")
        print("  " + "-" * 56)


if __name__ == "__main__":
    main()