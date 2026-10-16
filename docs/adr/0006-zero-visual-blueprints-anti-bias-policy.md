# 0006: Zero Visual Blueprints Anti-Bias Policy

## Context & Decision
When AI agent skills contain complete visual vector templates or pre-drawn SVG examples, LLMs strongly overfit to those shapes, generating repetitive, derivative variations rather than novel geometric artwork. We decided to enforce the **Zero Visual Blueprints Policy**: the skill documentation specifies mathematical formulas (Golden Ratio, Fibonacci scales, isometric axes, Euclidean tangents), architectural rules, and abstract empty tag hierarchies, but deliberately excludes pre-drawn shapes or visual clipart.

## Considered Options
- *Bundling Reference Blueprints (Webcam, Card, Loop)*: Rejected due to proven risk of biasing the agent toward carbon-copying template geometry across different user requests.

## Consequences
- Every SVG produced by the agent is designed completely from scratch based on the user's specific creative prompt.
- The agent relies on mathematical geometric principles rather than template cloning.
