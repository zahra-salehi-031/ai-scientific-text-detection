import openai
import pandas as pd
import time

# تنظیم API Key
client = openai.OpenAI(api_key="#")

# خواندن فایل اکسل ورودی
input_file = "gpt_out_scraped_links_Sociology.xlsx"
df = pd.read_excel(input_file)

# بررسی وجود ستون "Abstract"
if "Abstract" not in df.columns:
    raise ValueError("فایل اکسل باید ستونی با نام 'Abstract' داشته باشد.")

# قالب پرامپت پارافرایز
# Combined and optimized paraphrasing prompt template (multi-style, human-like, academic, dataset-ready)

prompt_template = ("Paraphrase the following academic abstract in a clear, formal, and scholarly tone. " 
                   "Maintain the original meaning and key points, but rephrase the sentences using different vocabulary and structure. " 
                   "Make sure the paraphrased version is fluent and suitable for academic publishing.\n\n" 
                   "Original Abstract:\n\"{}\""
)

# تابع درخواست به OpenAI
def paraphrase_abstract(original_abstract):
    prompt = prompt_template.format(original_abstract.strip())

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            timeout=30
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"

# پردازش گروهی
batch_size = 10
abstracts = df["Abstract"].tolist()
paraphrased_list = []
total_batches = len(abstracts) // batch_size + (1 if len(abstracts) % batch_size != 0 else 0)

for i in range(0, len(abstracts), batch_size):
    batch = abstracts[i:i + batch_size]
    batch_results = []

    for abs_text in batch:
        result = paraphrase_abstract(abs_text)
        batch_results.append(result)
        time.sleep(2)  # جلوگیری از محدودیت سرعت API

    paraphrased_list.extend(batch_results)

    progress = ((i // batch_size) + 1) / total_batches * 100
    print(f"✅ گروه {(i // batch_size) + 1}/{total_batches} انجام شد ({progress:.2f}% کامل)")

# اضافه کردن ستون جدید به دیتافریم
df["Abstract-Paraphrase"] = paraphrased_list

# ذخیره در فایل جدید
output_file = "paraph_2_gpt_out_scraped_links_Sociology.xlsx"
df.to_excel(output_file, index=False)

print(f"🔄 پارافرایز چکیده‌ها با موفقیت ذخیره شد در: {output_file}")
