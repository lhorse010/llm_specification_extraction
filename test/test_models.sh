source env.sh

# Define the array
models=("Claude-3.5-Sonnet" "Gemini-1.5-Pro" "GPT-4o" "Mixtral8x22b-Inst-FW" "Llama-3.1-405B-T" "Qwen-1.5-110B-T")

# Loop through the array
for model in "${models[@]}"; do
    echo "Processing model: $model"
    python llm_doc_spec_annotate.py $model ./px4_hold.json ./px4_hold_$model.result
done

