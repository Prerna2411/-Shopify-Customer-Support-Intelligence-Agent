# Project Report

## Objective

Build an AI-powered business workflow automation prototype for Shopify customer support.

## Architecture

The platform exposes a FastAPI endpoint that receives customer tickets and runs a multi-agent workflow. The current implementation uses local deterministic fallbacks so the project works without paid API keys, while the `models` package contains clear extension points for Groq and Gemini clients.

## Workflow

1. Customer submits a ticket through `POST /api/tickets`.
2. Supervisor decides which agents should run.
3. Intent agent classifies the support intent and priority.
4. Order agent loads matching Shopify-style order data.
5. Policy agent retrieves relevant policy documents.
6. Reasoning agent creates a grounded customer response.
7. Validation agent checks whether policy context was used.
8. Escalation service routes low-confidence or unverifiable cases to a human.

## Data

Policy documents live in `data/policies`. Sample orders live in `data/orders/orders.json`.

## Production Path

Replace local model fallbacks with real Groq and Gemini SDK calls, replace sample order JSON with Shopify Admin API calls, persist tickets in a database, and deploy the FastAPI service behind Nginx using the Docker files in `deployment`.
