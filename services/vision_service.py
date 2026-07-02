import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any
import datetime
from utils.logger import get_logger

logger = get_logger("vision_service")

class VisionService:
    def __init__(self):
        self.face_cascade = None
        # Proteção robusta contra falhas de carregamento de atributos binários no ecossistema OpenCV
        try:
            if hasattr(cv2, 'CascadeClassifier') and hasattr(cv2, 'data'):
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                logger.info("Classificador CascadeClassifier do OpenCV inicializado com sucesso.")
            else:
                logger.warning("Atributo CascadeClassifier indisponível no módulo cv2 atual.")
        except Exception as e:
            logger.error(f"Erro ao inicializar classificadores locais do OpenCV: {e}")

    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Executa o pipeline de Visão Computacional de forma determinística
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

            # Conversão segura para tons de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 1. Análise de Luminosidade
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

            # 3. Detecção Facial via Algoritmo de Viola-Jones (Apenas se carregado com sucesso)
            num_faces = 0
            if self.face_cascade is not None and not self.face_cascade.empty():
                try:
                    faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    num_faces = len(faces)
                except Exception as detect_err:
                    logger.error(f"Erro pontual na execução do detectMultiScale: {detect_err}")

            # 4. Extração Heurística de Cores Predominantes
            data = np.float32(img.reshape((-1, 3)))
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            flags = cv2.KMEANS_RANDOM_CENTERS
            try:
                _, _, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)
                dominant_bgr = centers[0].astype(int)
                cores_predominantes = f"RGB({dominant_bgr[2]}, {dominant_bgr[1]}, {dominant_bgr[0]})"
            except Exception:
                cores_predominantes = "Não determinado"

            analysis_result = {
                "descricao": "Captura processada via OpenCV Engine.",
                "objetos": "Análise clássica estrutural de bordas e contraste ativada.",
                "quantidade_pessoas": int(num_faces),
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
