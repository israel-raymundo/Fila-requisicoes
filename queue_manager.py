# queue_manager.py

import time
import uuid
import threading
from collections import deque

class QueueManager:
    def __init__(self, max_size: int = 10, process_time: float = 2.0):
        self.max_size     = max_size
        self.process_time = process_time
        self.queue        = deque()
        self.processing   = {}
        self.completed    = []
        self.rejected     = []
        self.lock         = threading.Lock()

    def adicionar(self, user_id: str) -> dict:
        with self.lock:
            total_ocupado = len(self.queue) + len(self.processing)

            if total_ocupado >= self.max_size:
                tarefa = {
                    "id":        str(uuid.uuid4())[:8],
                    "user_id":   user_id,
                    "status":    "rejeitada",
                    "motivo":    "Fila cheia",
                    "criado_em": time.time()
                }
                self.rejected.append(tarefa)
                return {"allowed": False, "tarefa": tarefa,
                        "message": "❌ Fila cheia! Tente novamente em instantes."}

            posicao = len(self.queue) + 1
            tarefa = {
                "id":        str(uuid.uuid4())[:8],
                "user_id":   user_id,
                "status":    "aguardando",
                "criado_em": time.time(),
                "posicao":   posicao
            }
            self.queue.append(tarefa)

            thread = threading.Thread(target=self._processar, args=(tarefa,))
            thread.daemon = True
            thread.start()

            return {"allowed": True, "tarefa": tarefa,
                    "message": f"✅ Tarefa #{tarefa['id']} adicionada. Posição: {posicao}"}

    def _processar(self, tarefa: dict):
        # Aguarda até ser o primeiro da fila
        while True:
            with self.lock:
                if self.queue and self.queue[0]["id"] == tarefa["id"]:
                    self.queue.popleft()
                    tarefa["status"]      = "processando"
                    tarefa["iniciado_em"] = time.time()
                    self.processing[tarefa["id"]] = tarefa
                    break
            time.sleep(0.1)

        time.sleep(self.process_time)

        with self.lock:
            tarefa["status"]       = "concluída"
            tarefa["concluido_em"] = time.time()
            tarefa["duracao"]      = round(tarefa["concluido_em"] - tarefa["iniciado_em"], 2)
            self.processing.pop(tarefa["id"], None)
            self.completed.insert(0, tarefa)
            self.completed = self.completed[:50]

    def status(self) -> dict:
        with self.lock:
            return {
                "fila":        list(self.queue),
                "processando": list(self.processing.values()),
                "concluidas":  self.completed[:10],
                "rejeitadas":  self.rejected[-10:],
                "total_fila":  len(self.queue),
                "total_proc":  len(self.processing),
                "total_conc":  len(self.completed),
                "total_rej":   len(self.rejected),
                "max_size":    self.max_size
            }

    def resetar(self):
        with self.lock:
            self.queue.clear()
            self.processing.clear()
            self.completed.clear()
            self.rejected.clear()