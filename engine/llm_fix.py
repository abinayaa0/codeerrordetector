import subprocess


def repair_xml_with_llm(xml: str) -> dict:
    prompt = f"""
You are an expert XML repair tool.
Your goal is to fix the structural errors in the provided XML snippet (e.g., missing closing tags).
Preserve the existing content and values as much as possible.
Return ONLY the corrected XML string. Do not include markdown formatting or explanations.

Input XML:
{xml}
"""

    MAX_RETRIES = 2
    
    for attempt in range(MAX_RETRIES + 1):
        print(f"DEBUG: Calling Ollama (Attempt {attempt + 1}/{MAX_RETRIES + 1})...")
        try:
            result = subprocess.run(
                ["ollama", "run", "qwen2.5-coder"],
                input=prompt,
                text=True,
                capture_output=True,
                check=False
            )
            repaired = result.stdout.strip()
            print(f"DEBUG: Ollama output received. Length: {len(repaired)}")
            
            if result.stderr:
                 print(f"DEBUG: Ollama stderr: {result.stderr}")

            # If we got a valid-looking response, correct
            if repaired and repaired != "UNFIXABLE":
                return {
                    "repaired_xml": repaired,
                    "explanation": "XML structure repaired using Qwen2.5-Coder"
                }
            
            print(f"DEBUG: Attempt {attempt + 1} failed: Empty or UNFIXABLE output.")

        except FileNotFoundError:
            print("DEBUG: Ollama executable not found.")
            return {
                "repaired_xml": None,
                "explanation": "Ollama executable not found"
            }
        except Exception as e:
            print(f"DEBUG: Exception calling Ollama: {e}")
            # Continue to next attempt on exception
    
    # If all retries failed
    return {
        "repaired_xml": None,
        "explanation": "LLM could not safely repair XML after retries"
    }
