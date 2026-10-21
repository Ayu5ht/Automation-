# Autonomous AI Agent & Multi-Platform Workflow Orchestrator

## 📌 Project Overview
An intelligent backend automation engine built in Python that utilizes the **OpenAI API** to analyze unstructured operational data and dynamically orchestrate multi-step workflows across **n8n** and **Make** via **REST APIs**. 

This system eliminates manual ticket triage by autonomously classifying intent, analyzing sentiment, drafting responses, and routing structured JSON payloads to the appropriate automation platform.

## 🛠️ Tech Stack
* **AI & LLM:** OpenAI API (`gpt-4o-mini` with Structured JSON Outputs)
* **Backend & CLI:** Python 3, `requests`, `json`
* **Workflow Automation:** n8n (Technical Escalations), Make.com (CRM & Customer Comms)
* **Integration:** RESTful Webhooks

## ⚙️ System Architecture
1. **Python CLI Ingestion Engine:** Polls or ingests raw customer inquiries and operational tasks.
2. **OpenAI Triage Agent:** Evaluates urgency, sentiment, and category via system prompt engineering, returning a strict JSON schema.
3. **Dynamic Webhook Router:** 
   * Routes `High Urgency` & `Technical_Bug` payloads to an **n8n** webhook to automate Jira ticket creation and Slack engineering alerts.
   * Routes `Sales_Lead` & `General_Support` payloads to a **Make** webhook to automate CRM entry and draft email responses.

## 📸 Workflow Architecture Screenshots
*(Upload screenshots of your n8n canvas, Make scenario, and Python terminal output here)*
