import os
import tempfile
from utils.logger import get_logger

logger = get_logger("audio_service")

class AudioService:
    def __init__(self):
        self.model = None
        self.initialized = False

    def _lazy_init(self):
        """Inicialização preguiçosa otimizada para o nível gratuito do Render."""
        if not self.initialized:
            try:
                from faster_whisper import WhisperModel
                logger.info("Inicializando modelo de áudio leve (int8) para instâncias gratuitas...")
                # Mudamos compute_type para int8 para rodar perfeitamente com menos de 512MB de RAM
                self.model = WhisperModel("tiny", device="cpu", compute_type="int8")
                self.initialized = True
                logger.info("Modelo de transcrição carregado com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao carregar dependências do faster-whisper: {e}", exc_info=True)
                raise e
            
    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """
        Salva o stream em arquivo temporário estruturado e processa a transcrição
        fonética retornando o texto traduzido e consolidado.
        """
        if not audio_bytes:
            return ""
            
        try:
            self._lazy_init()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_bytes)
                temp_path = temp_audio.name

            logger.info(f"Processando arquivo de áudio temporário: {temp_path}")
            segments, info = self.model.transcribe(temp_path, beam_size=1)
            
            transcription = " ".join([segment.text for segment in segments])
            
            try:
                os.remove(temp_path)
            except OSError:
                pass
                
            logger.info("Transcrição de áudio concluída com sucesso.")
            return transcription.strip()
            
        except Exception as e:
            logger.error(f"Erro durante a execução da transcrição fonética: {e}", exc_info=True)
            return f"[Erro na transcrição automática]: {str(e)}"