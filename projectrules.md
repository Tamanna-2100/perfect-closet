# Perfect Closet Engineering Guidelines

- Architecture: Python FastAPI backend + Next.js frontend.
- Do NOT use LLMs for color classification or skin detection; use deterministic CV routines.
- Maintain strict typing (Pydantic models in Python, TypeScript interfaces in frontend).
- Do not rewrite whole files when fixing errors—only modify target functions.
- Every color value must be converted to CIELAB space before calculating distances.