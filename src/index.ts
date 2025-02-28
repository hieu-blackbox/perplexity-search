#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError
} from "@modelcontextprotocol/sdk/types.js";
import axios, { AxiosError } from "axios";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

// Define interface for error response
interface PerplexityErrorResponse {
  error?: string;
  message?: string;
}

export class PerplexityServer {
  private server: Server;
  private maxTokens: number = 8192;
  private temperature: number = 0.2;
  private model: string;

  constructor() {
    // Get model from command line args
    const modelIndex = process.argv.indexOf('--model');
    const model = modelIndex !== -1 ? process.argv[modelIndex + 1] : 'sonar-pro';
    
    if (!['sonar', 'sonar-pro'].includes(model)) {
      throw new Error('Invalid model. Must be either "sonar" or "sonar-pro"');
    }
    
    this.model = model;
    console.error(`Using Perplexity model: ${this.model}`);
    
    this.server = new Server({
      name: "perplexity-search-server",
      version: "0.1.0"
    }, {
      capabilities: {
        tools: {}
      }
    });

    this.setupHandlers();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error("[MCP Error]", error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupHandlers(): void {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [{
          name: "search",
          description: "Perform a web search using Perplexity's API, which provides detailed and contextually relevant results with citations. By default, no time filtering is applied to search results.",
          inputSchema: {
            type: "object",
            properties: {
              query: {
                type: "string",
                description: "The search query to perform"
              },
              search_recency_filter: {
                type: "string",
                description: "Filter search results by recency (options: month, week, day, hour). If not specified, no time filtering is applied.",
                enum: ["month", "week", "day", "hour"]
              }
            },
            required: ["query"]
          }
        }]
      };
    });

    // Handle tool execution
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      switch (request.params.name) {
        case "search": {
          const { 
            query, 
            search_recency_filter
          } = request.params.arguments as {
            query: string;
            search_recency_filter?: string;
          };

          try {
            const payload: any = {
              model: this.model,
              messages: [
                {
                  role: "user",
                  content: query
                }
              ],
              max_tokens: this.maxTokens,
              temperature: this.temperature
            };

            // Add optional parameters if provided
            if (search_recency_filter) {
              payload.search_recency_filter = search_recency_filter;
            }

            console.error(`Using model: ${this.model}, max_tokens: ${this.maxTokens}, temperature: ${this.temperature}`);

            const response = await axios.post('https://api.perplexity.ai/chat/completions', payload, {
              headers: {
                'Authorization': `Bearer ${process.env.PERPLEXITY_API_KEY!}`,
                'Content-Type': 'application/json'
              }
            });
            
            // Format the response to only include content and citations
            const formattedResponse = {
              content: response.data.choices[0].message.content,
              citations: response.data.citations || []
            };
            
            return {
              content: [{
                type: "text",
                text: JSON.stringify(formattedResponse, null, 2)
              }]
            };
          } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
              const axiosError = error as AxiosError<PerplexityErrorResponse>;
              const errorData = axiosError.response?.data;
              const errorMessage = errorData?.error || errorData?.message || axiosError.message;
              
              return {
                content: [{
                  type: "text", 
                  text: `Perplexity API error: ${errorMessage}`
                }],
                isError: true
              };
            }
            throw error;
          }
        }

        default:
          throw new McpError(
            ErrorCode.MethodNotFound,
            `Unknown tool: ${request.params.name}`
          );
      }
    });
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error(`Perplexity Search MCP server running on stdio`);
  }
}

// Start the server
const server = new PerplexityServer();
server.run().catch(console.error); 