import json

input_file = 'dataset_for_fine_tuning.json'    # Tu archivo fuente con la lista JSON
output_file = 'faq_dataset_rag_ready.jsonl' # Archivo final compatible con Vertex AI RAG

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(output_file, 'w', encoding='utf-8') as f_out:
    for item in data:
        instruction = item.get("instruction", "").strip()
        user_input = item.get("input", "").strip()
        output = item.get("output", "").strip()

        full_context = f"Instruction: {instruction}\n\nUser Input: {user_input}\n\nOutput: {output}"

        doc = {
            "id": f"doc-{item['metadata'].get('id', 'unknown')}",
            "title": instruction if instruction else user_input[:50],
            "content": full_context,
            "metadata": item.get("metadata", {})
        }

        f_out.write(json.dumps(doc, ensure_ascii=False) + '\n')

print(f"File converted successfully to {output_file}")
