import openai
import time
from anthropic import Anthropic
from llamaai import LlamaAPI
import json
import json_repair
import re
import logging

# Placeholder for logger setup, recommend configuring this properly
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LLM:
#   def __init__(self, default_model="openai-gpt-4o"):
    def __init__(self, default_model="anthropic-claude-3-5-sonnet-20240620"):
        self.openai_client = None
        self.openrouter_client = None
        self.anthropic_client = None
        self.llamaai_client = None
        self.default_model = default_model

    def init_openai(self, organization, api_key):
        if self.openai_client is None:
            self.openai_client = openai.OpenAI(organization=organization, api_key=api_key)

    def init_openrouter(self, api_key):
        if self.openrouter_client is None:
            self.openrouter_client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    def init_anthropic(self, api_key):
        if self.anthropic_client is None:
            self.anthropic_client = Anthropic(api_key=api_key)

    def init_llamaai(self, api_key):
        if self.llamaai_client is None:
            self.llamaai_client = openai.OpenAI(api_key = api_key, base_url = "https://api.llama-api.com")
            #LlamaAPI(api_key)

    def clean_json(self, text):
        return json_repair.clean_json(text)

    def _construct_message_content(self, text_content, image_urls=None):
        """
        Constructs message content that supports both text and images.
        
        Args:
            text_content: The text content of the message
            image_urls: List of image URLs to include (optional)
            
        Returns:
            Either a string (text only) or a list with text and image objects
        """
        if not image_urls:
            return text_content
        
        content = [{"type": "text", "text": text_content}]
        
        for image_url in image_urls:
            content.append({
                "type": "image_url",
                "image_url": {"url": image_url}
            })
        
        return content
        
    def query(self, user_query, system_message="", max_tokens=1024, temperature=0.7, model=None, full_object=False, image_urls=None):
        content = self._construct_message_content(user_query, image_urls)
        messages = [{"role": "user", "content": content}]
        return self.query_messages(messages, system_message=system_message, max_tokens=max_tokens, temperature=temperature, model=model, full_object=full_object)

    def jquery(self, user_query, system_message="", max_tokens=1024, temperature=1.0, model=None, image_urls=None):
#       print("\n\n\n" + user_query + "\n\n\n")
        content = self._construct_message_content(user_query, image_urls)
        messages = [{"role": "user", "content": content}]
        response = self.query_messages(messages, system_message=system_message, max_tokens=max_tokens, temperature=temperature, model=model)
        json_data = None
        try:
            cleaned_json_str = json_repair.clean_json(response)
            json_data = json.loads(cleaned_json_str)
        except Exception as repair_err:
             logger.error(f"JSON query failed: {repair_err}")
             raise ValueError("Could not extract or repair JSON from LLM response") from repair_err
        return json_data

    def query_messages(self, messages, system_message="", max_tokens=1024, temperature=1.0, model=None, full_object=False):
        if model is None:
            model = self.default_model

#        logger.info("\n\n\n-----------------------------------------------------------------------------------")
#        logger.info(f"Querying model: {model}\n")
        
        # Log the system message
 #       if system_message:
 #           logger.info(f"System message: {system_message}\n")
 #       else:
 #           logger.info("System message: (empty)\n")

        # Log the latest message
        if messages:
            latest_message = messages[-1]
            content = latest_message.get('content', '')
            role = latest_message.get('role', 'unknown')
            
            # Handle both string content and list content (for images)
            if isinstance(content, list):
                # Extract text parts for logging
                text_parts = [item.get('text', '') for item in content if item.get('type') == 'text']
                content_preview = ' '.join(text_parts)
                image_count = len([item for item in content if item.get('type') == 'image_url'])
                if image_count > 0:
                    content_preview += f" [+{image_count} image(s)]"
            else:
                content_preview = str(content)
            
  #          logger.info(f"Latest message ({role}): {content_preview}")        
  #      logger.info("-----------------------------------------------------------------------------------\n\n\n")

        parts = model.split('-', 1)
        if len(parts) != 2:
            raise ValueError("Model identifier must include both provider and model name, separated by a hyphen.")
    
        provider, model_name = parts

        if provider == "openai":
            return self._query_openai(messages, system_message, max_tokens, temperature, model_name, full_object)
        elif provider == "openrouter":
            return self._query_openrouter(messages, system_message, max_tokens, temperature, model_name, full_object)
        elif provider == "anthropic":
            return self._query_anthropic(messages, system_message, max_tokens, temperature, model_name, full_object)
        elif provider == "llamaai":
            return self._query_llamaai(messages, system_message, max_tokens, temperature, model_name, full_object)
        else:
            raise ValueError(f"Unsupported provider or model format: {model}")

    def _query_openai(self, messages, system_message, max_tokens, temperature, model, full_object=False):
        if self.openai_client is None:
            raise ValueError("OpenAI client is not initialized. Please call init_openai first.")
        
        combined_messages = [{"role": "system", "content": system_message}]
        combined_messages.extend(messages)
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=combined_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            if full_object:
                return response
            return response.choices[0].message.content.strip()
        except openai.RateLimitError:
            print("The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again.")
            time.sleep(10)
            return self._query_openai(messages, system_message, max_tokens, temperature, model)
        except openai.BadRequestError:
            print("Bad request error.")
            return None
        except Exception as e:
            print(f"An unexpected exception occurred: {str(e)}")
            return None

    def _query_openrouter(self, messages, system_message, max_tokens, temperature, model, full_object=False):
        if self.openrouter_client is None:
            raise ValueError("OpenRouter client is not initialized. Please call init_openrouter first.")
        
        combined_messages = [{"role": "system", "content": system_message}]
        combined_messages.extend(messages)
        
        try:
            response = self.openrouter_client.chat.completions.create(
                model=model,
                messages=combined_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            #print(response)
            if full_object:
                return response
            return response.choices[0].message.content.strip()
        except openai.RateLimitError:
            print("The OpenRouter API rate limit has been exceeded. Waiting 10 seconds and trying again.")
            time.sleep(10)
            return self._query_openrouter(messages, system_message, max_tokens, temperature, model)
        except openai.BadRequestError:
            print("Bad request error.")
            return None
        except Exception as e:
            print(f"An unexpected exception occurred: {str(e)}")
            return None

    def _query_anthropic(self, messages, system_message, max_tokens, temperature, model, full_object=False):
        if self.anthropic_client is None:
            raise ValueError("Anthropic client is not initialized. Please call init_anthropic first.")
        
#       combined_messages = [{"role": "system", "content": system_message}]
#       combined_messages.extend(messages)
        
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                system=system_message
            )
            if full_object:
                return response
            return response.content[0].text.strip()
        except Exception as e:
            print(f"An unexpected exception occurred: {str(e)}")
            return None

    def _query_llamaai(self, messages, system_message, max_tokens, temperature, model, full_object=False):
        if self.llamaai_client is None:
            raise ValueError("LlamaAI client is not initialized. Please call init_llamaai first.")
        
        combined_messages = [{"role": "system", "content": system_message}]
        combined_messages.extend(messages)
        
        try:
            response = self.llamaai_client.chat.completions.create(
                model=model,
                messages=combined_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            if full_object:
                return response
            return response.choices[0].message.content.strip()
        except openai.RateLimitError:
            print("The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again.")
            time.sleep(10)
            return self._query_openai(messages, system_message, max_tokens, temperature, model)
        except openai.BadRequestError:
            print("Bad request error.")
            return None
        except Exception as e:
            print(f"An unexpected exception occurred: {str(e)}")
            return None

class LLMTools:
    @staticmethod
    def extract_chunk(input_string: str, begin_marker: str, end_marker: str) -> str:
        """
        Extracts the text content between two specified marker strings.

        Args:
            input_string: The string to search within.
            begin_marker: The string that marks the beginning of the chunk.
            end_marker: The string that marks the end of the chunk.

        Returns:
            The extracted text chunk, stripped of leading/trailing whitespace.
            Returns None if the markers are not found or if there's no content between them.
        """
        # Escape the markers to ensure they are treated as literal strings in the regex,
        # especially if they contain special regex characters.
        pattern = re.escape(begin_marker) + r'(.*?)' + re.escape(end_marker)
        
        # re.DOTALL allows '.' to match newline characters as well
        match = re.search(pattern, input_string, re.DOTALL)
        
        if match:
            # group(1) returns the content captured by the first (and only) capturing group (.*?)
            return match.group(1).strip()
        else:
            # Return None if no match is found
            return None

class LLMThread:
    def __init__(self, llm_instance: 'LLM', system_message: str = ""):
        self.llm = llm_instance
        self.history = []
        self.system_message = system_message
        self.commands = {} # Stores command handlers and their descriptions
        if system_message:
            pass
        # Register the built-in help command
        self.register_command("help", self._handle_help_command, help_description="Lists available commands and their descriptions.")

    def _handle_help_command(self, llm: 'LLM', messages: list, system_message: str, 
                             max_tokens: int, temperature: float, model: str, 
                             command_prompt: str, image_urls: list = None) -> str:
        """Handles the /help command by listing available commands and their descriptions."""
        if not self.commands or len(self.commands) == 0:
            return "No commands are currently registered."
        
        if command_prompt: # User asked for help on a specific command
            target_command = command_prompt.strip()
            if target_command.startswith('/'):
                target_command = target_command[1:]
            if target_command in self.commands:
                desc = self.commands[target_command].get("description", "No description provided.")
                return f"Help for /{target_command}: {desc}"
            else:
                return f"Command /{target_command} not found."

        output_lines = ["Available commands:"]
        for name, details in sorted(self.commands.items()):
            description = details.get("description", "No description provided.")
            output_lines.append(f"  /{name} - {description}")
        
        return "\n".join(output_lines)

    def register_command(self, command_name: str, handler_function: callable, help_description: str = ""):
        """
        Registers a slash command, its handler function, and a help description.
        The command_name should be without the leading slash (e.g., "poem").
        The handler_function will be called with keyword arguments (see query method).
        help_description is a one-line string describing the command for /help output.
        Note: Command handlers now receive an additional image_urls parameter.
        """
        if command_name.startswith('/'):
            command_name = command_name[1:]
        if ' ' in command_name or not command_name:
            raise ValueError("Command name cannot contain spaces and must not be empty.")
        self.commands[command_name] = {"handler": handler_function, "description": help_description}

    def query(self, user_query: str, max_tokens: int = 1024, temperature: float = 0.7, model: str = None, image_urls: list = None):
        # Construct message content with potential images
        content = self.llm._construct_message_content(user_query, image_urls)
        self.history.append({"role": "user", "content": content})
        
        response_content = None
        is_command_handled = False

        if user_query.startswith("/") and len(user_query) > 1 and not user_query[1].isspace():
            parts = user_query.split(" ", 1)
            command_name_with_slash = parts[0]
            command_name = command_name_with_slash[1:]
            command_prompt = parts[1] if len(parts) > 1 else ""

            if command_name in self.commands:
                command_data = self.commands[command_name]
                handler_func = command_data["handler"]
                try:
                    response_content = handler_func(
                        llm=self.llm,
                        messages=self.history,
                        system_message=self.system_message,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        model=model,
                        command_prompt=command_prompt,
                        image_urls=image_urls
                    )
                    is_command_handled = True
                except Exception as e:
                    logger.error(f"Error executing command {command_name}: {e}")
                    response_content = f"Error executing command '{command_name}': {e}"
                    is_command_handled = True

        if not is_command_handled:
            # If not a command or command not found/error during setup, query the LLM
            response_content = self.llm.query_messages(
                messages=self.history, # History includes the user_query
                system_message=self.system_message,
                max_tokens=max_tokens,
                temperature=temperature,
                model=model,
                full_object=False 
            )

        # Add LLM/command response to history
        if response_content is not None:
            # Ensure response is a string before adding to history
            self.history.append({"role": "assistant", "content": str(response_content)})
        
        return response_content

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
        # System message is preserved

    def export_to_json(self) -> str:
        """Exports the thread's history and system message to a JSON string."""
        thread_data = {
            "system_message": self.system_message,
            "history": self.history
        }
        return json.dumps(thread_data, indent=2)

    @classmethod
    def load_from_json(cls, llm_instance: 'LLM', json_string: str) -> 'LLMThread':
        """
        Loads a thread from a JSON string.
        Requires an LLM instance to be provided.
        Command handlers are not part of the export/import and would need to be re-registered.
        """
        thread_data = json.loads(json_string)
        system_message = thread_data.get("system_message", "")
        history = thread_data.get("history", [])
        
        new_thread = cls(llm_instance, system_message)
        new_thread.history = history
        # Note: new_thread.commands will be empty. Handlers must be re-registered if needed.
        return new_thread

if __name__ == "__main__":
    # This is an example usage of the LLM and LLMThread classes.
    # IMPORTANT: You need to initialize at least one LLM provider with your API key.
    # For example, for Anthropic (which is the default in LLM class):
    # my_llm.init_anthropic(api_key="YOUR_ANTHROPIC_API_KEY")
    # Or for OpenAI:
    # my_llm.init_openai(organization="YOUR_ORG_ID", api_key="YOUR_OPENAI_API_KEY")

    # 1. Define a command handler function
    def poem_command_handler(llm: LLM, messages: list, system_message: str, 
                             max_tokens: int, temperature: float, model: str, 
                             command_prompt: str, image_urls: list = None) -> str:
        """Handles the /poem command. Uses the LLM to generate a poem."""
        if not command_prompt:
            return "Please provide a topic for the poem. Usage: /poem <topic>"
        
        # You can use the provided llm instance to make a new query
        # Or, you could potentially use parts of the existing messages if relevant
        poem_request = f"Write a short poem about: {command_prompt}"
        
        # Using the llm.query method for simplicity here.
        # Note: This creates a new, isolated query to the LLM for the poem.
        # It doesn't use the ongoing thread's history for this specific internal LLM call,
        # but the command itself IS part of the main thread's history.
        try:
            poem = llm.query(user_query=poem_request, 
                             system_message="You are a poetic assistant.", # Optional: specific system message for this task
                             max_tokens=max_tokens, 
                             temperature=temperature, 
                             model=model,
                             image_urls=image_urls) # Use the same model/params or override
            return f"Here's a poem about '{command_prompt}':\n\n{poem}"
        except Exception as e:
            logger.error(f"Error generating poem: {e}")
            return "Sorry, I encountered an error while trying to write the poem."

    # 2. Initialize LLM and LLMThread
    # Replace with your actual API key and provider initialization
    print("Initializing LLM...")
    # IMPORTANT: Provide your API key here for the provider you want to use.
    # The default model is "anthropic-claude-3-5-sonnet-20240620"
    # If you don't have an Anthropic key, change default_model in LLM class
    # and initialize the corresponding provider (e.g. init_openrouter).
    llm_instance = LLM() 
    try:
        # Attempt to initialize Anthropic. User needs to provide their key.
        # THIS IS A PLACEHOLDER - REPLACE with your actual key or use a different provider.
        # os.environ.get("ANTHROPIC_API_KEY") is a common way to get keys.
        # For this example, we'll assume it might fail if not set.
        llm_instance.init_anthropic(api_key="YOUR_ANTHROPIC_API_KEY_HERE_OR_FROM_ENV") 
        print("Anthropic client initialized (using placeholder key). REPLACE with your actual key.")
    except ValueError as e:
        print(f"Failed to initialize default Anthropic client: {e}")
        print("Please ensure your API key is correctly set for a provider (e.g., Anthropic, OpenAI, OpenRouter).")
        print("Falling back to a dummy mode for demonstration if no provider is active.")
        # Add a dummy query method if no real client is up, to let example run without keys for structure demo.
        def dummy_query_messages(messages, system_message, max_tokens, temperature, model, full_object=False):
            if messages and messages[-1]["role"] == "user" and messages[-1]["content"].startswith("/poem"):
                return "Roses are red, violets are blue, this is a dummy poem, because no API key for you."
            return "This is a dummy LLM response as no API key was provided or initialization failed."
        llm_instance.query_messages = dummy_query_messages
        llm_instance.default_model = "dummy-model"


    main_thread = LLMThread(llm_instance, system_message="You are a helpful assistant.")

    # 3. Register the command (now with a help description)
    main_thread.register_command("poem", poem_command_handler, help_description="Writes a poem about a given topic.")
    print("Registered /poem command.")

    # 4. Interact with the thread
    print("\n--- Starting conversation ---")

    user_q1 = "Hello, how are you today?"
    print(f"\nUser: {user_q1}")
    response1 = main_thread.query(user_q1)
    print(f"Assistant: {response1}")

    user_q2 = "/poem a curious cat"
    print(f"\nUser: {user_q2}")
    response2 = main_thread.query(user_q2)
    print(f"Assistant: {response2}")

    user_q_help = "/help"
    print(f"\nUser: {user_q_help}")
    response_help = main_thread.query(user_q_help)
    print(f"Assistant: {response_help}")

    user_q3 = "What was the topic of the poem?"
    print(f"\nUser: {user_q3}")
    response3 = main_thread.query(user_q3)
    print(f"Assistant: {response3}")

    # Example with image support
    user_q4 = "Can you describe what's in this image?"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    print(f"\nUser: {user_q4}")
    print(f"Image URL: {image_url}")
    response4 = main_thread.query(user_q4, image_urls=[image_url])
    print(f"Assistant: {response4}")

    # 5. Optionally, export the thread
    exported_thread_json = main_thread.export_to_json()
    print("\n--- Exported Thread JSON ---")
    print(exported_thread_json)

    # Example of loading (requires llm_instance)
    # new_thread = LLMThread.load_from_json(llm_instance, exported_thread_json)
    # new_thread.register_command("poem", poem_command_handler) # Commands need re-registration
    # print("\n--- Loaded thread and asked for another poem ---")
    # response_loaded = new_thread.query("/poem the moon")
    # print(f"Assistant (loaded thread): {response_loaded}")

    print("\n--- Full History from main_thread ---")
    for entry in main_thread.get_history():
        print(f"{entry['role'].title()}: {entry['content']}")

