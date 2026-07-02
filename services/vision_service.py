import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any
import datetime
from utils.logger import get_logger

logger = get_logger("vision_service")

class VisionService:
    def __init__(self):
        # Inicializa classificadores em cascata pré-treinados do OpenCV para detecção nativa local
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Executa o pipeline completo de Visão Computacional de forma determinística
        calculando propriedades matemáticas, espaciais e heurísticas da imagem.
        """
        try:
            now = datetime.datetime.now()
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Incapaz de decodificar o arquivo de imagem fornecido.")

            height, width, _ = img.shape
            resolution = f"{width}x{height}"

            # 1. Análise de Luminosidade
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
            if mean_brightness < 50:
                luminosidade = "Baixa / Escuro"
            elif mean_brightness > 200:
                luminosidade = "Muito Alta / Superexposto"
            else:
                luminosidade = "Normal / Balanceada"

            # 2. Análise de Nitidez usando a Variância Laplaciana
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            nitidez = "Alta / Focado" if laplacian_var > 100 else "Baixa / Desfocado"

            # 3. Detecção Facial via Algoritmo de Viola-Jones
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            num_faces = len(faces)

            # 4. Extração Heurística de Cores Predominantes
            data = np.float32(img.reshape((-1, 3)))
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            flags = cv2.KMEANS_RANDOM_CENTERS
            _, _, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)
            dominant_bgr = centers[0].astype(int)
            cores_predominantes = f"RGB({dominant_bgr[2]}, {dominant_bgr[1]}, {dominant_bgr[0]})"

            # Estrutura preparada para extensões e integrações futuras com LLMs/Vision APIs
            analysis_result = {
                "descricao": "Captura processada via OpenCV Engine.",
                "objetos": "Análise clássica estrutural de bordas e contraste ativada.",
                "quantidade_pessoas": int(num_faces),  # Base aproximada por detecção de faces
                "rostos": int(num_faces),
                "idade": "Não disponível (Requer API externa de deep learning)",
                "emocao": "Não disponível (Requer API externa de deep learning)",
                "cores": cores_predominantes,
                "luminosidade": luminosidade,
                "nitidez": f"{nitidez} (Score: {int(laplacian_var)})",
                "resolution": resolution,
                "data": now.strftime("%Y-%m-%d"),
                "horario": now.strftime("%H:%M:%S")
            }
            
            logger.info("Pipeline de análise de imagem processado com sucesso.")
            return analysis_result

        except Exception as e:
            logger.error(f"Falha crítica no processamento da imagem: {e}", exc_info=True)
            raise e