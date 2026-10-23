
import openai
import pandas as pd
import time

# تنظیم API Key
client = openai.OpenAI(api_key="#")

# خواندن فایل اکسل ورودی
input_file = "out_scraped_links_Psychology.xlsx"
df = pd.read_excel(input_file)

# بررسی وجود ستون "Title"
if "Title" not in df.columns:
    raise ValueError("فایل اکسل باید ستونی با نام 'Title' داشته باشد.")

# پرامپت دلخواه
prompt_template = (
    "Generate a 150–200 word academic abstract for the provided research title. "
    "Follow all instructions exactly:\n"
    "1. Write in a formal academic tone, avoiding conversational or promotional language.\n"
    "2. Begin with a strong, academically engaging opening sentence that introduces the broader context of the research.\n"
    "3. Clearly state the research problem, its significance, and the motivation without repeating key terms.\n"
    "4. Summarize the methodology concisely, focusing only on essential steps.\n"
    "5. Present the core findings and contributions using varied vocabulary and precise academic wording.\n"
    "6. Avoid:\n"
    "   - repeating the same nouns, verbs, or phrases more than twice,\n"
    "   - starting consecutive sentences with the same word,\n"
    "   - generic expressions such as 'this study aims to' or 'the results show that'.\n"
    "7. Use diverse sentence structures and maintain a cohesive logical flow from problem → method → findings → contribution.\n"
    "8. Ensure the writing is original, non-template-based, and stylistically varied.\n"
    "Return only the abstract, with no explanations, notes, or commentary.\n"
    "Research Title: '{}'"
)


# تابع درخواست به OpenAI
def generate_abstract(title):
    prompt = prompt_template.format(title)

    try:
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            timeout=30
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# پردازش گروهی
batch_size = 10
titles = df["Title"].tolist()
abstracts = []  # مقداردهی اولیه
total_batches = len(titles) // batch_size + (1 if len(titles) % batch_size != 0 else 0)

for i in range(0, len(titles), batch_size):
    batch = titles[i:i + batch_size]
    batch_abstracts = []

    for title in batch:
        abstract = generate_abstract(title)
        batch_abstracts.append(abstract)
        time.sleep(2)

    abstracts.extend(batch_abstracts)

    # نمایش درصد پیشرفت
    progress = ((i // batch_size) + 1) / total_batches * 100
    print(f"✅ پردازش {(i // batch_size) + 1}/{total_batches} گروه انجام شد ({progress:.2f}% تکمیل شده)")

# اگر لیست `abstracts` مقدار ندارد، مقدار پیش‌فرض تنظیم شود
if not abstracts:
    abstracts = ["Error: No abstracts generated"] * len(titles)

# اضافه کردن چکیده‌ها به دیتافریم
df["Abstract-gpt3-5"] = abstracts

# ذخیره در فایل جدید
output_file = "gpt_new_perampt_out_scraped_links_Psychology.xlsx"
df.to_excel(output_file, index=False)

print(f"چکیده‌ها با موفقیت ذخیره شدند در: {output_file}")