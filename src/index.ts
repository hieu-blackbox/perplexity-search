#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
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

const maxTokens: number = 8192;
const temperature: number = 0.2;
const modelIndex = process.argv.indexOf('--model');
const model = modelIndex !== -1 ? process.argv[modelIndex + 1] : 'sonar-pro';

if (!['sonar', 'sonar-pro'].includes(model)) {
  throw new Error('Invalid model. Must be either "sonar" or "sonar-pro"');
}

console.error(`Using Perplexity model: ${model}`);

server = new Server({
  name: "perplexity-search-server",
  version: "0.1.0"
}, {
  capabilities: {
    tools: {}
  }
});

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
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
server.setRequestHandler(CallToolRequestSchema, async (request) => {
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
          model: model,
          messages: [
            {
              role: "user",
              content: query
            }
          ],
          max_tokens: maxTokens,
          temperature: temperature
        };

        // Add optional parameters if provided
        if (search_recency_filter) {
          payload.search_recency_filter = search_recency_filter;
        }

        console.error(`Using model: ${model}, max_tokens: ${maxTokens}, temperature: ${temperature}`);

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


// Start the server
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";
const app = express();

let transport: SSEServerTransport;

app.get("/sse", (req, res) => {
    console.log("Received connection");
    transport = new SSEServerTransport("/messages", res);
    server.connect(transport);
});

app.post("/messages", (req, res) => {
    console.log("Received message handle message");
    if (transport) {
        transport.handlePostMessage(req, res);
    }
});

const PORT = process.env.PORT || 3001;
    app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
