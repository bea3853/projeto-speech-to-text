import csv
import io
import json
from typing import List, Any

def convert_to_csv(records: List[Any]) -> bytes:
    """Converte instâncias do modelo de dados do repositório em payload CSV delimitado."""
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    
    # Cabeçalho estruturado
    writer.writerow(["ID", "Data Criacao", "Caminho Imagem", "Descricao", "Objetos", "Pessoas", "Rostos", "Luminosidade", "Nitidez", "Transcricao"])
    
    for r in records:
        writer.writerow([
            r.id, r.created_at, r.image_path, r.descricao, r.objetos, 
            r.quantidade_pessoas, r.rostos, r.luminosidade, r.nitidez, r.transcricao
        ])
        
    return output.getvalue().encode("utf-8")

def convert_to_json(records: List[Any]) -> bytes:
    """Consolida os registros passados em um array purificado JSON stringificado em bytes."""
    data_list = []
    for r in records:
        data_list.append({
            "id": r.id,
            "created_at": str(r.created_at),
            "image_path": r.image_path,
            "descricao": r.descricao,
            "objetos": r.objetos,
            "quantidade_pessoas": r.quantidade_pessoas,
            "rostos": r.rostos,
            "cores": r.cores,
            "luminosidade": r.luminosidade,
            "nitidez": r.nitidez,
            "transcricao": r.transcricao
        })
    return json.dumps(data_list, indent=2, ensure_ascii=False).encode("utf-8")