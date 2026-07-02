import os
import uuid
import datetime
from typing import List, Optional, Dict, Any
from database.connection import SessionLocal
from repositories.analise_repository import AnaliseRepository
from models.analise import AnaliseModel
from services.vision_service import VisionService
from services.audio_service import AudioService
from config.settings import UPLOAD_FOLDER
from utils.logger import get_logger

logger = get_logger("app_controller")

class AppController:
    def __init__(self):
        self.vision_service = VisionService()
        self.audio_service = AudioService()

    def handle_capture_and_analysis(self, image_bytes: bytes, audio_bytes: Optional[bytes] = None) -> Optional[AnaliseModel]:
        """Coordena o fluxo de salvar arquivos físicos, extrair insights de IA e persistir no banco."""
        db = SessionLocal()
        repository = AnaliseRepository(db)
        try:
            # 1. Salvar arquivo físico de imagem de forma única
            filename = f"capture_{uuid.uuid4().hex}.jpg"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            with open(file_path, "wb") as f:
                f.write(image_bytes)

            # 2. Executar análises técnicas paralelas
            analysis_data = self.vision_service.analyze_image(image_bytes)
            
            transcription_text = ""
            if audio_bytes and len(audio_bytes) > 0:
                transcription_text = self.audio_service.transcribe_audio(audio_bytes)

            # 3. Mapear dados processados para a Entidade relacional
            model_entry = AnaliseModel(
                image_path=file_path,
                descricao=analysis_data["descricao"],
                objetos=analysis_data["objetos"],
                quantidade_pessoas=analysis_data["quantidade_pessoas"],
                rostos=analysis_data["rostos"],
                idade=analysis_data["idade"],
                emocao=analysis_data["emocao"],
                cores=analysis_data["cores"],
                luminosidade=analysis_data["luminosidade"],
                nitidez=analysis_data["nitidez"],
                transcricao=transcription_text,
                json_resultado=analysis_data
            )

            saved_record = repository.save(model_entry)
            return saved_record
        except Exception as e:
            logger.error(f"Erro controlado no fluxo do caso de uso da aplicação: {e}", exc_info=True)
            return None
        finally:
            db.close()

    def fetch_records(self, search: Optional[str] = None, start: Optional[datetime.date] = None, end: Optional[datetime.date] = None) -> List[AnaliseModel]:
        db = SessionLocal()
        repository = AnaliseRepository(db)
        try:
            return repository.get_all(search, start, end)
        finally:
            db.close()

    def remove_record(self, record_id: int) -> bool:
        db = SessionLocal()
        repository = AnaliseRepository(db)
        try:
            # Buscar path para limpar o arquivo físico do disco rígido local
            record = db.query(AnaliseModel).filter(AnaliseModel.id == record_id).first()
            if record and os.path.exists(record.image_path):
                try:
                    os.remove(record.image_path)
                except OSError:
                    pass
            return repository.delete(record_id)
        finally:
            db.close()

    def update_audio_transcription(self, record_id: int, audio_bytes: bytes) -> Optional[str]:
        """Atualiza ou adiciona uma transcrição de áudio a um registro existente."""
        db = SessionLocal()
        try:
            record = db.query(AnaliseModel).filter(AnaliseModel.id == record_id).first()
            if record:
                text = self.audio_service.transcribe_audio(audio_bytes)
                record.transcricao = text
                db.commit()
                return text
            return None
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao injetar áudio em registro histórico: {e}", exc_info=True)
            return None
        finally:
            db.close()

    def clear_audio_transcription(self, record_id: int) -> bool:
        db = SessionLocal()
        try:
            record = db.query(AnaliseModel).filter(AnaliseModel.id == record_id).first()
            if record:
                record.transcricao = ""
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            return False
        finally:
            db.close()