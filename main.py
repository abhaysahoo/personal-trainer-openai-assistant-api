import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

client = openai.OpenAI()
model = "gpt-4o-mini"

# create our assistant
personal_trainer_assis = client.beta.assistants.create(
    name="Personal Trainer",
    instructions= """You are the best personal trainer and nutritionist who knows how to get clients to build lean muscles.
You have trained high-caliber athletes and movie stars.""",
    model=model
)

assistant_id = personal_trainer_assis.id
print(assistant_id)

# thread
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "I want to wake up early in the morning at around 5 am and do Yoga. How do I wake up early?"
        }
    ]
)

thread_id = thread.id
print(thread_id)

assistant_id = "asst_EUvMbbwMQA2r6fxvUjgwsoXr"
thread_id = "thread_DJ0na1YLIXYD8O9myGyV9Dpm"

# create message 
message = "Give me examples of a few sports celebrities and their discipline to waking up early"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
)

# run our assistant 
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as an adult of aged 25" 
)


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.
    :param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# Steps --- logs 
run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread_id,
    run_id=run.id,
)

print(f"Steps---> {run_steps.data[0]}")

