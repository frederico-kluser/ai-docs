# LLM API showdown: Usage limits and pricing in 2025

The landscape of large language model APIs has evolved significantly through early 2025, with providers competing on both pricing and accessibility. This comparison examines the current usage constraints and pricing structures across major LLM API providers, highlighting key differences that impact developers' choices for production deployments.

## Free tier offerings: From generous to nonexistent

Each provider takes a dramatically different approach to free usage, with some offering substantial free tokens while others provide no free tier at all:

| Provider | Free Monthly Tokens | Rate Limits (Free Tier) | Models Available | Additional Notes |
|----------|---------------------|-------------------------|------------------|-----------------|
| Anthropic | $10 maximum usage | 5 RPM, 20K ITPM, 8K OTPM | Claude 3.5 Sonnet | 300K tokens daily limit |
| DeepSeek | No official free tier | N/A | N/A | Available on Azure preview at $0 |
| Google Gemini | Unlimited for free models | Gemini 2.5 Flash: 10 RPM, 250K TPM, 500 RPD | All models with limits | Pro models: 2 RPM, 32K TPM, 50 RPD |
| OpenAI | $5 initial credit + Free Daily Tokens (1-10M) | Severely restricted | Limited access | Free tokens require data sharing |
| Azure OpenAI | $200 credit (30 days) | 1K TPM for all models | Limited models | Free trial users have zero quota for advanced models |
| Ollama | Unlimited (open source) | Hardware-dependent | All available models | Local deployment only |

## Paid tier limits: Balancing throughput and cost

Significant variations exist in how providers structure their paid tiers and the maximum throughput allowed:

| Provider | Tier Structure | Standard Tier RPM | Standard Tier TPM | Enterprise Level Maximum |
|----------|----------------|-------------------|-------------------|--------------------------|
| Anthropic | Usage-based ($5-$400) | 50 RPM | Varies by model | Custom via sales |
| DeepSeek | No explicit tiers | "No constraints" | Unlimited (claimed) | Custom arrangements available |
| Google Gemini | 3 tiers based on usage | Gemini 2.5 Flash: 1K RPM | 1M TPM | Tier 3: 5K+ RPM, 10M+ TPM |
| OpenAI | 5 tiers based on spending | Tier 1: Varies by model | Varies by model | Tier 5: ~10K RPM, 30M TPM |
| Azure OpenAI | Default and Enterprise | GPT-4o: 2.7K RPM | 450K TPM | GPT-4o: 180K RPM, 30M TPM |
| Ollama | N/A (self-hosted) | Configurable (default: 4) | Hardware-dependent | Hardware-dependent |

## Simultaneous requests: The concurrency challenge

Rate limits significantly impact application architecture, with wide variations in allowed concurrent processing:

| Provider | Concurrent Request Limit | Rate Limiting Method | Burst Capability | Queue System |
|----------|--------------------------|----------------------|------------------|--------------|
| Anthropic | Free tier: 1, Paid: Based on RPM | Token bucket algorithm | Yes | Message Batches API: 100K max queue |
| DeepSeek | No specific limit mentioned | No explicit rate limits | N/A | Connections remain open during high traffic |
| Google Gemini | Free: 3 concurrent sessions | Per-project limits | Limited | TPM and RPM limits enforced |
| OpenAI | Based on tier and model | Three-level (RPM, RPD, TPM) | Limited | GPT-4o Tier 5: 5B batch queue limit |
| Azure OpenAI | Based on RPM/TPM ratio | Varies by model family | Limited | Batch API has separate queue limits |
| Ollama | Default: 4 per model | Simple counter | No | Max queue: 512 requests |

## Pricing: The token economy

**Model pricing varies dramatically across providers, with up to 30x differences for comparable capabilities:**

| Provider | Input Token Price (per million) | Output Token Price (per million) | Context Window Size | Special Pricing Features |
|----------|--------------------------------|----------------------------------|---------------------|-------------------------|
| Anthropic | Claude 3 Opus: $15<br>Claude 3 Sonnet: $3<br>Claude 3 Haiku: $0.25 | Claude 3 Opus: $75<br>Claude 3 Sonnet: $15<br>Claude 3 Haiku: $1.25 | 200K tokens all models | Prompt caching available |
| DeepSeek | DeepSeek-V3: $0.27<br>DeepSeek-R1: $0.55 | DeepSeek-V3: $1.10<br>DeepSeek-R1: $2.19 | 64K tokens | Off-peak discounts<br>Cache hit discount: 74-75% |
| Google Gemini | Gemini 2.5 Pro: $1.25-$2.50<br>Gemini 2.5 Flash: $0.15<br>Gemini 1.5 Flash-8B: $0.0375 | Gemini 2.5 Pro: $10-$15<br>Gemini 2.5 Flash: $0.60<br>Gemini 1.5 Flash-8B: $0.15-$0.30 | Gemini 2.5 Pro: 1M tokens<br>Gemini 2.0 Flash: 1M tokens | Tiered pricing for large contexts<br>Context storage fees |
| OpenAI | GPT-4.1: $2<br>GPT-4o: $3<br>GPT-4o mini: $0.15 | GPT-4.1: $8<br>GPT-4o: $10<br>GPT-4o mini: $0.60 | GPT-4.1: 1M tokens<br>GPT-4o: 128K tokens | 75% discount for cached prompts<br>50% batch discount |
| Azure OpenAI | Similar to OpenAI with variations by deployment type | Similar to OpenAI with variations by deployment type | Varies by model | Global/Data Zone/Regional deployments<br>Provisioned Throughput Units |
| Ollama | $0 (local compute costs only) | $0 (local compute costs only) | Default: 4K (configurable) | Hardware costs only |

## Other usage constraints: The fine print

Beyond core limits and pricing, providers implement additional constraints that significantly impact application design:

| Provider | Special Limitations | Recent Changes | Key Advantages |
|----------|---------------------|----------------|----------------|
| Anthropic | Token counting varies for cached prompts | New Max Plan with higher rate limits<br>Claude 3.7 Sonnet with extended thinking | 128K output tokens in extended thinking mode<br>Custom spend limits per workspace |
| DeepSeek | Minimum cache size: 64 tokens<br>30-minute connection timeout | Upgraded to DeepSeek-V3<br>Released under MIT License | No explicit rate limits<br>Significant cache discounts |
| Google Gemini | Grounding with Search: 500 free/day then $35 per 1K<br>Image generation: $0.03/image | Gemini 2.5 Pro introduced May 2025<br>Tiered pricing for larger contexts | Multimodal capabilities included<br>Generous free tier |
| OpenAI | Performance degrades with >10 concurrent requests<br>Audio processing has separate pricing | New GPT-4.1 models (April 2025)<br>83-90% price drop over 16 months | Batch API with 50% discount<br>75% cached prompt discount |
| Azure OpenAI | 30 resource instances max per region<br>Performance tiers based on monthly usage | New deployment options (Global/Data Zone)<br>Removal of model deployment restrictions | Three deployment types for compliance needs<br>Spillover feature for traffic management |
| Ollama | Hardware-dependent limitations<br>Model-specific licenses may apply | New context length configuration<br>Improved function calling support | Completely configurable<br>No usage-based costs |

## Conclusion

Provider selection remains highly dependent on specific use cases. Google Gemini offers the most generous free tier for developers, while DeepSeek claims unlimited throughput for high-volume applications. Anthropic provides balance with moderate pricing and clear rate limits, while OpenAI continues aggressive price reductions. Azure adds compliance options through regional deployment types, and Ollama provides a cost-effective option for those willing to manage their own infrastructure. Consider your specific throughput, budget, and feature requirements when making your selection.