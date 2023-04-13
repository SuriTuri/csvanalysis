import os
import openai
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["csvfile"]
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
            summary, detailed = analyze_data(df)
            return jsonify({"summary": summary, "detailed": detailed})
        else:
            return jsonify({"error": "Invalid file type. Please upload a CSV file."})
    return render_template("index.html")

def analyze_data(df):
    # Create a prompt for the OpenAI API
    prompt = f"データサイエンティストとして、次のCSVデータを分析してください。サマリーと詳細の2つに分けて説明してください。サマリーでは重要な要素を箇条書きで説明し、詳細では端的に分かりやすく説明してください。また、データに外れ値が含まれている場合は、外れ値を含むデータと、外れ値を除いたデータでそれぞれ分析結果を出してください。分析の目的は、エンゲージメントが高い傾向のあるコンテンツを特定し、マーケティング的な視点で活用できる情報を得ることです。\n\n{df.to_csv(index=False)}\n\n分析結果："

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the summary and detailed results from the response
    result = response.choices[0].text.strip()
    summary, detailed = result.split("\n\n", 1)

    return summary, detailed

if __name__ == "__main__":
    app.run()