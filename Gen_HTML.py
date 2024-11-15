from openai import OpenAI

#API CONFIG
OPENAI_API_KEY = "WPROWADŹ KLUCZ API"
client = OpenAI(api_key=OPENAI_API_KEY)

#funkcja budująca artykuł
def BuildArtykul(system_prompt, user_build_prompt, article_content):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # Rola systemu: Określenie wytycznych dla generowania HTML
            {"role": "system", "content": system_prompt},
            # Rola użytkownika: Przekazanie promptu i artykułu
            {"role": "user", "content": user_build_prompt + "\n"+"article: "+ article_content}
        ]
    )
    output = completion.choices[0].message.content
    return output

#funkcja organizująca artykuł
def OrganizeArticle(system_prompt,user_organize_prompt, html_content):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_organize_prompt + "\n" + html_content}
        ]
    )
    output = completion.choices[0].message.content
    return remove_code_fences(output)

#w przypadku 4o 
def remove_code_fences(content):
    return content.replace("```html", "").replace("```", "")

system_prompt = (
    "You are an expert assistant who specializes in generating well-structured HTML code. "
    "Your task is to take the article content and structure it into HTML format that is easy to read and visually appealing. "
    "Ensure the output is correctly indented and well-organized."
)

user_build_prompt = (
    "Generate HTML code from the following article_content "
    "Do not include <html>, <head>, <body>, or ```html and ``` tags and any CSS or JavaScript code. "
    "First line of the article is <header h1>, THERE IS ONLY ONE HEADER, for the others: If the text in the document occupies only one line and is short (max 6 words), it should be wrapped in an <h2> tag. If the text spans multiple lines, it should be wrapped in a <p> tag. Pack all in Wrap everything in <div class=container>"
    "If content in <h2> is longer than 14 words convert it to <p>, and do not generate any text thats is not included article, do not create <h2> by yourself" 
    "think carefully and place maximum three images in three relevant sections of the article that match the paragraph content using this format  <figure> <img src='image_placeholder.jpg' alt= Detailed prompt"
    "Ensure the alt text is a detailed prompt in English for generating a high-quality image in the style of DALL-E. The prompt should accurately represent the paragraph's content with specific visual elements, such as objects, background setting, lighting, color schemes, and any other relevant details to create a visually rich and descriptive image."
    "For example, instead of a general description like 'An image representing the ethical challenges of AI,' write a detailed prompt such as 'A futuristic cityscape at dusk with humanoid robots and humans interacting, soft ambient lighting, a blend of metallic and warm hues, showing harmony and tension between technology and humanity.'"
    "add <figcaption> maximum 6 words summary of the image described in the alt (in Polish, max 6 words) </figcaption> </figure>."
    "If there is a * before text write in italic, do not remove * symbol"
    )

user_organize_prompt = (
    "Take the generated HTML and reorganize it with semantic HTML5 tags for improved readability and structure: "
    "1. Place tags: (<article> after the <header>) (<footer> at the end line), add sections IMPORTANT"
)



#LoadArticle
with open("artykulbase.txt", "r", encoding="utf-8") as file:
    article_content = file.read()

#Step 1: Build HTML
InitialHTML = BuildArtykul(system_prompt, user_build_prompt, article_content)

#Step 2: Organize HTML
OrganizedHTML = OrganizeArticle(system_prompt, InitialHTML, user_organize_prompt)

#Save
with open("artykul.html", "w", encoding="utf-8") as output_file:
    output_file.write(OrganizedHTML)



#LOG
print("HTML wygenerowany i zapisany do artykul.html")
