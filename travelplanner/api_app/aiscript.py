import os
#from dotenv import load_dotenv
from groq import Groq
def fill_description(destination_name: str) -> str:
    """Retrieve country of origin of landmark
    Args:
        landmark (str): Landmark like the Eiffel Tower
    Returns:
        str: Country of origin of the landmark, like France
    """
    #print(fill_description("Eiffel Tower"))
    client = Groq(
        api_key="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"                    #os.getenv("API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Give a description of {destination_name} in 2 sentences."
            }
        ],
        model="llama3-8b-8192",
    )
    groq_answer = chat_completion.choices[0].message.content
    # Test whether groq has finished the sentence with a point or other non-alphabetic character.
    # If so, then delete this character from the answer.
    return groq_answer
if __name__ == "__main__":
    print(fill_description("Koh Phangan"))